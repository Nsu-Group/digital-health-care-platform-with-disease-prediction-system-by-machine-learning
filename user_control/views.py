import pickle
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from appointment_control.models import AppointmentModel, RatingModel
from article_control.models import ArticleModel
from patient_community_control.models import CommunityPostModel
from user_control.decorators import *
from user_control.forms import *
from user_control.utils import calculate_age


@unauthenticated_user
def home_view(request):
    return render(request, "index.html")


@unauthenticated_user
def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user and user.is_doctor:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("doctor-dashboard")

            elif user and user.is_patient:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("patient-dashboard")
            else:
                messages.error(request, "Email or Password is incorrect.")
                return redirect("login")
        else:
            return render(request, "authentication/login.html", {"form": form})

    form = LoginForm()
    context = {"form": form}
    return render(request, "authentication/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


@unauthenticated_user
def doctor_signup_view(request):
    if request.method == "POST":
        doctor_form = DoctorRegistrationForm(request.POST)
        if doctor_form.is_valid():
            doctor_form.save()
            email = request.POST["email"]
            password = request.POST["password1"]
            user = authenticate(request, email=email, password=password)
            user.is_doctor = True
            user.save()
            DoctorModel.objects.create(user=user)
            login(request, user)
            return redirect("doctor-dashboard")
        else:
            context = {"doctor_form": doctor_form}
            return render(request, "authentication/doctor-signup.html", context)
    else:
        doctor_form = DoctorRegistrationForm()

    context = {"doctor_form": doctor_form}
    return render(request, "authentication/doctor-signup.html", context)


@unauthenticated_user
def patient_signup_view(request):
    if request.method == "POST":
        patient_form = PatientRegistrationForm(request.POST)
        if patient_form.is_valid():
            patient_form.save()
            email = request.POST["email"]
            password = request.POST["password1"]
            user = authenticate(request, email=email, password=password)
            user.is_patient = True
            user.save()
            PatientModel.objects.create(user=user)
            login(request, user)
            return redirect("patient-dashboard")
        else:
            context = {"patient_form": patient_form}
            return render(request, "authentication/patient-signup.html", context)
    else:
        patient_form = PatientRegistrationForm()

    context = {"patient_form": patient_form}
    return render(request, "authentication/patient-signup.html", context)


@login_required(login_url="login")
@show_to_doctor()
def doctor_dashboard(request):
    user = request.user
    profile = DoctorModel.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "pages/user-control/doctor-dashboard.html", context)


@login_required(login_url="login")
@show_to_patient()
def patient_dashboard(request):
    user = request.user
    profile = PatientModel.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "pages/user-control/patient-dashboard.html", context)


@login_required(login_url="login")
def doctor_profile_view(request, pk):
    is_self = False
    user = UserModel.objects.get(id=pk)

    if request.user == user:
        is_self = True

    doctor_profile = DoctorModel.objects.get(user=user)

    date_joined = calculate_age(user.date_joined)

    incomplete_profile = False
    if (
            not doctor_profile.bio
            or not doctor_profile.gender
            or not doctor_profile.blood_group
            or not doctor_profile.date_of_birth
            or not doctor_profile.phone
            or not doctor_profile.NID
            or not doctor_profile.specialization
            or not doctor_profile.BMDC_regNo
    ):
        incomplete_profile = True

    articles = ArticleModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(
        doctor=doctor_profile, is_complete=True
    )

    is_pending = False
    if request.user.is_patient:
        patient = PatientModel.objects.get(user=request.user)
        appointments = AppointmentModel.objects.filter(
            patient=patient,
            doctor=doctor_profile,
            is_accepted=False,
            is_canceled=False,
            is_complete=False,
        )
        if appointments.count() > 0:
            is_pending = True

    ratings = RatingModel.objects.filter(doctor=doctor_profile)

    context = {
        "user": user,
        "is_self": is_self,
        "profile": doctor_profile,
        "date_joined": date_joined,
        "completed_appointment_list": completed_appointments,
        "completed_appointments": completed_appointments.count(),
        "incomplete_profile": incomplete_profile,
        "articles": articles,
        "total_posts": articles.count(),
        "is_pending": is_pending,
        "ratings": ratings,
    }
    return render(request, "pages/user-control/doctor-profile.html", context)


@login_required(login_url="login")
def patient_profile_view(request, pk):
    is_self = False

    user = UserModel.objects.get(id=pk)
    if request.user == user:
        is_self = True

    has_access = True

    profile = PatientModel.objects.get(user=user)

    date_joined = calculate_age(user.date_joined)

    age = None
    if profile.date_of_birth:
        age = calculate_age(profile.date_of_birth)

    community_posts = CommunityPostModel.objects.filter(author=user)[:4]
    completed_appointments = AppointmentModel.objects.filter(
        patient=profile, is_complete=True
    )

    incomplete_profile = False
    if (
            not profile.gender
            or not profile.blood_group
            or not profile.date_of_birth
            or not profile.phone
            or not profile.height
            or not profile.weight
            or not profile.address
    ):
        incomplete_profile = True

    context = {
        "user": user,
        "is_self": is_self,
        "has_access": has_access,
        "age": age,
        "profile": profile,
        "date_joined": date_joined,
        "incomplete_profile": incomplete_profile,
        "community_posts": community_posts,
        "completed_appointments": completed_appointments.count(),
        "total_posts": community_posts.count(),
    }
    return render(request, "pages/user-control/patient-profile.html", context)


@login_required(login_url="login")
def doctor_edit_profile(request):
    user = request.user
    profile = DoctorModel.objects.get(user=user)

    form = DoctorEditProfileForm(instance=profile)
    if request.method == "POST":
        form = DoctorEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("doctor-profile", user.id)
        else:
            # print errors
            print(form.errors)
            return redirect("doctor-edit-profile")

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "pages/user-control/edit-profile.html", context)


@login_required(login_url="login")
def patient_edit_profile(request):
    user = request.user
    profile = PatientModel.objects.get(user=user)

    form = PatientEditProfileForm(instance=profile)
    if request.method == "POST":
        form = PatientEditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("patient-profile", user.id)
        else:
            return redirect("patient-edit-profile")

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "pages/user-control/edit-profile.html", context)


def terms_view(request):
    return render(request, "pages/utils/terms.html")

def privacy_view(request):
    return render(request, "pages/utils/privacy.html")

def about_view(request):
    return render(request, "pages/utils/about.html")

def contact_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        email_add = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        FeedbackModel.objects.create(
            name=name, email=email_add, subject=subject, message=message
        )

        messages.success(request, "Feedback sent successfully.")

        return render(request, "pages/utils/contact.html")

    return render(request, "pages/utils/contact.html")


@login_required(login_url="login")
def account_settings_view(request):
    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == "POST":
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            user.save()
            return redirect("account-settings")

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("account-settings")
        else:
            context = {
                "information_form": information_form,
                "password_form": password_form,
            }
            return render(request, "pages/user-control/account-settings.html", context)
    context = {
        "information_form": information_form,
        "password_form": password_form,
    }
    return render(request, "pages/user-control/account-settings.html", context)


ALL_ZEROS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
SYMPTOM_LIST = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting',
                'burning_micturition', 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety',
                'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat',
                'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
                'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite',
                'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever',
                'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression',
                'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
                'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
                'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
                'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum',
                'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads',
                'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
                'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
DISEASES = {
    'Fungal Infection': 15,
    'Allergy': 4,
    'GERD': 16,
    'Chronic Cholestasis': 9,
    'Drug Reaction': 14,
    'Peptic Ulcer Disease': 33,
    'AIDS': 1,
    'Diabetes ': 12,
    'Gastroenteritis': 17,
    'Bronchial Asthma': 6,
    'Hypertension ': 23,
    'Migraine': 30,
    'Cervical Spondylosis': 7,
    'Paralysis (brain hemorrhage)': 32,
    'Jaundice': 28,
    'Malaria': 29,
    'Chicken pox': 8,
    'Dengue': 11,
    'Typhoid': 37,
    'hepatitis A': 40,
    'Hepatitis B': 19,
    'Hepatitis C': 20,
    'Hepatitis D': 21,
    'Hepatitis E': 22,
    'Alcoholic hepatitis': 3,
    'Tuberculosis': 36,
    'Common Cold': 10,
    'Pneumonia': 34,
    'Dimorphic hemmorhoids(piles)': 13,
    'Heart attack': 18,
    'Varicose veins': 39,
    'Hypothyroidism': 26,
    'Hyperthyroidism': 24,
    'Hypoglycemia': 25,
    'Osteoarthristis': 31,
    'Arthritis': 5,
    '(vertigo) Paroymsal  Positional Vertigo': 0,
    'Acne': 2,
    'Urinary tract infection': 38,
    'Psoriasis': 35,
    'Impetigo': 27,
}
asdf = [15, 4, 16, 9, 14, 33, 1, 12, 17, 6, 23, 30, 7, 32, 28, 29, 8,
        11, 37, 40, 19, 20, 21, 22, 3, 36, 10, 34, 13, 18, 39, 26, 24, 25,
        31, 5, 0, 2, 38, 35, 27]


def disease_prediction_view(request):
    form = DiseasePredictionForm()

    if request.method == "POST":
        form = DiseasePredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            loaded_model = pickle.load(open("user_control/disease_prediction_model.sav", "rb"))
            inputs = []
            for k, v in data.items():
                inputs.append(v)

            print(inputs)
            for i in range(0, len(SYMPTOM_LIST)):
                for j in inputs:
                    if j == SYMPTOM_LIST[i]:
                        ALL_ZEROS[i] = 1

            input_test = ALL_ZEROS

            predict = loaded_model.predict([input_test])
            predicted = predict[0]
            print(predicted)

            # check in DISEASES dict and get the key
            disease = [k for k, v in DISEASES.items() if v == predicted]
            
            context = {
                "form": form,
                "disease": disease
            }

            return render(request, "pages/utils/disease-prediction.html", context)

    context = {
        "form": form,
    }

    return render(request, "pages/utils/disease-prediction.html", context)
