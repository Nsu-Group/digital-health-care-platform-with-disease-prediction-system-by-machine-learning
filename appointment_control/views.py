from django.conf import Settings
from django.core.mail import send_mail
from django.template import loader
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from user_control.decorators import show_to_doctor, show_to_patient
from user_control.utils import calculate_age
from .forms import *
from .models import AppointmentModel, RatingModel
from user_control.models import (
    UserModel,
    DoctorModel,
    PatientModel,
    SpecializationModel,
)
from .utils import filter_appointment_list, render_to_pdf


@login_required(login_url="login")
@show_to_patient()
def patient_appointment_home_view(request):
    user = request.user
    patient = PatientModel.objects.get(user=user)
    appointments = AppointmentModel.objects.filter(patient=patient)
    filtered_appointments = filter_appointment_list(appointments)

    context = {
        "pending_appointments": filtered_appointments[0],
        "upcoming_appointments": filtered_appointments[1],
        "rejected_appointments": filtered_appointments[2],
        "completed_appointments": filtered_appointments[3],
    }
    return render(request, "pages/appointment/patient-appointment-home.html", context)


@login_required(login_url="login")
@show_to_doctor()
def doctor_appointment_home_view(request):
    user = request.user
    doctor = DoctorModel.objects.get(user=user)
    appointments = AppointmentModel.objects.filter(doctor=doctor)

    pending_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == False
           and appointment.is_canceled == False
           and appointment.is_complete == False
    ]
    upcoming_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == True
           and appointment.is_canceled == False
           and appointment.is_complete == False
    ]
    rejected_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == False
           and appointment.is_canceled == True
           and appointment.is_complete == False
    ]
    completed_appointments = [
        appointment
        for appointment in appointments
        if appointment.is_accepted == True
           and appointment.is_canceled == False
           and appointment.is_complete == True
    ]

    context = {
        "pending_appointments": pending_appointments,
        "upcoming_appointments": upcoming_appointments,
        "rejected_appointments": rejected_appointments,
        "completed_appointments": completed_appointments,
    }
    return render(request, "pages/appointment/doctor-appointment-home.html", context)


@login_required(login_url="login")
@show_to_patient()
def make_appointment_view(request, pk):
    doctor = DoctorModel.objects.get(user=UserModel.objects.get(id=pk))
    patient = PatientModel.objects.get(user=request.user)

    form = PatientAppointmentForm()
    if request.method == "POST":
        form = PatientAppointmentForm(request.POST)
        payment_method = request.POST.get("payment_method")
        amount = request.POST.get("amount")
        sent_number = request.POST.get("sent_number")
        trx_id = request.POST.get("trx_id")
        print(payment_method, sent_number, trx_id)
        if form.is_valid():
            print(form.cleaned_data)
            new_appointment = form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.doctor = doctor
            new_appointment.department = doctor.specialization
            new_appointment.save()
            PaymentModel.objects.create(
                appointment=new_appointment,
                amount=amount,
                payment_method=payment_method,
                phone_number=sent_number,
                transaction_id=trx_id,
            )
            return redirect("appointment-details", new_appointment.id)
        else:
            context = {
                "patient": patient,
                "doctor": doctor,
                "form": form,
            }
            return render(request, "pages/appointment/make-appointment.html", context)

    context = {
        "patient": patient,
        "doctor": doctor,
        "form": form,
    }
    return render(request, "pages/appointment/make-appointment.html", context)


@login_required(login_url="login")
@show_to_patient()
def patient_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    form = PatientAppointmentForm(instance=appointment)
    if request.method == "POST":
        form = PatientAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment.save()
            return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/patient-update-appointment.html", context)


@login_required(login_url="login")
@show_to_doctor()
def doctor_appointment_update_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    form = DoctorAppointmentForm(instance=appointment)
    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            appointment.is_accepted = True
            appointment.save()
            return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/doctor-update-appointment.html", context)


@login_required(login_url="login")
@show_to_patient()
def appointment_delete_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":
        appointment.delete()
        return redirect("patient-appointment-home")

    context = {
        "appointment": appointment,
    }
    return render(request, "pages/appointment/delete-appointment.html", context)


@login_required(login_url="login")
@show_to_doctor()
def appointment_reject_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":
        appointment.is_canceled = True
        appointment.save()
        return redirect("appointment-details", appointment.id)

    context = {
        "appointment": appointment,
    }
    return render(request, "pages/appointment/reject-appointment.html", context)


@login_required(login_url="login")
def appointment_detail_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    payment = PaymentModel.objects.get(appointment=appointment)
    is_pending = False
    if (
            appointment.is_accepted is False
            and appointment.is_canceled is False
            and appointment.is_complete is False
    ):
        is_pending = True

    is_upcoming = False
    if (
            appointment.is_accepted is True
            and appointment.is_canceled is False
            and appointment.is_complete is False
    ):
        is_upcoming = True

    is_complete = False
    prescription = None
    if appointment.is_complete:
        is_complete = True
        prescription = PrescriptionModel.objects.get(appointment=appointment)

    rating = None
    rated = False
    if appointment.is_complete and RatingModel.objects.filter(appointment=appointment).exists():
        rated = True
        rating = RatingModel.objects.get(appointment=appointment)

    context = {
        "request_user": request.user,
        "appointment": appointment,
        "payment": payment,
        "is_pending": is_pending,
        "is_complete": is_complete,
        "is_upcoming": is_upcoming,
        "prescription": prescription,
        "rating": rating,
        "rated": rated,
    }
    return render(request, "pages/appointment/appointment-details.html", context)


@login_required(login_url="login")
@show_to_doctor()
def write_prescription_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    form = PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()

            appointment.is_complete = True
            appointment.save()
            return redirect("appointment-details", appointment.id)
        else:
            context = {
                "appointment": appointment,
                "form": form,
            }
            return render(
                request, "pages/appointment/appointment-details.html", context
            )

    context = {
        "appointment": appointment,
        "form": form,
    }
    return render(request, "pages/appointment/write-prescription.html", context)



@login_required(login_url="login")
def email_prescription_view(request, pk):
    prescription = PrescriptionModel.objects.get(id=pk)
    appointment = prescription.appointment
    doctor = appointment.doctor
    patient = appointment.patient
    
    subject = "Care and Cure - Prescription"
    email_from = "careandcure810@gmail.com"
    recipient_list = [patient.user.email]

    context = {
        "patient": patient,
        "doctor": doctor,
        "appointment": appointment,
        "prescription": prescription,
    }
    msg_plain = loader.render_to_string('email-templates/prescription/prescription.txt', context)
    msg_html = loader.render_to_string('email-templates/prescription/prescription.html', context)

    send_mail(subject, msg_plain, email_from, recipient_list, fail_silently=True, html_message=msg_html)
    return redirect("appointment-details", appointment.id)


@login_required(login_url="login")
def pdf_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)

    patient = PatientModel.objects.get(user=appointment.patient.user)

    prescription = PrescriptionModel.objects.get(appointment=appointment)

    age = None
    if patient.date_of_birth:
        age = calculate_age(patient.date_of_birth)

    context = {
        "age": age,
        "appointment": appointment,
        "prescription": prescription,
    }
    pdf = render_to_pdf("pages/appointment/pdf.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


def appointment_doctor_list_view(request):
    specializations = SpecializationModel.objects.all()
    doctors = DoctorModel.objects.all()
    doctors = [doctor for doctor in doctors if doctor.specialization is not None]

    context = {
        "specializations": specializations,
        "doctors": doctors,
    }
    return render(request, "pages/appointment/doctors-list.html", context)


@login_required(login_url="login")
def send_email_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    doctor = appointment.doctor
    patient = appointment.patient
    message = request.POST.get("message")
    print(message)
    subject = "Care and Cure - Appointment Follow Up"
    email_from = doctor.user.email
    recipient_list = [patient.user.email]

    context = {
        "appointment": appointment,
        "doctor": doctor,
        "patient": patient,
        "message": message,
    }
    msg_plain = loader.render_to_string('email-templates/follow-up/follow-up.txt', context)
    msg_html = loader.render_to_string('email-templates/follow-up/follow-up.html', context)

    send_mail(subject, msg_plain, email_from, recipient_list, fail_silently=True, html_message=msg_html)
    return redirect("appointment-details", appointment.id)


@login_required(login_url="login")
def rate_doctor_view(request, pk):
    appointment = AppointmentModel.objects.get(id=pk)
    comment = request.POST.get("comment")
    rating = int(request.POST.get("rating").strip())

    RatingModel.objects.create(
        patient=appointment.patient,
        doctor=appointment.doctor,
        appointment=appointment,
        comment=comment,
        rating=rating
    )
    doctor_ratings = RatingModel.objects.filter(doctor=appointment.doctor)
    doctor_ratings_sum = sum([int(doctor_rating.rating) for doctor_rating in doctor_ratings])
    doctor_avg_rating = doctor_ratings_sum / len(doctor_ratings)
    appointment.doctor.rating = doctor_avg_rating
    appointment.doctor.save()
    return redirect("appointment-details", appointment.id)
