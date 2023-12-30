from django.urls import path

from .views import *


urlpatterns = [
    path("", home_view, name="home"),
    path("auth/login", login_view, name="login"),
    path("auth/logout", logout_view, name="logout"),
    path("auth/doctor-registration", doctor_signup_view, name="doctor-register"),
    path("auth/patient-registration", patient_signup_view, name="patient-register"),
    path("doctor-dashboard", doctor_dashboard, name="doctor-dashboard"),
    path("patient-dashboard", patient_dashboard, name="patient-dashboard"),
    path("doctor-profile/<str:pk>", doctor_profile_view, name="doctor-profile"),
    path("patient-profile/<str:pk>", patient_profile_view, name="patient-profile"),
    path("update-doctor-profile", doctor_edit_profile, name="doctor-edit-profile"),
    path("update-patient-profile", patient_edit_profile, name="patient-edit-profile"),
    path("auth/account-settings", account_settings_view, name="account-settings"),
    path("disease-prediction", disease_prediction_view, name="disease-prediction"),
    path("terms-and-conditions", terms_view, name="terms"),
    path("privacy-policy", privacy_view, name="privacy"),
    path("about-us", about_view, name="about"),
    path("contact-us", contact_view, name="contact"),
]
