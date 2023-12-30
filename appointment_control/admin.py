from django.contrib import admin
from .models import *


class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "department",
        "date",
        "time",
        "is_accepted",
        "is_canceled",
        "is_complete",
        "created_at",
    ]
    list_filter = ["date", "is_accepted", "is_canceled", "is_complete"]
    search_fields = ["patient", "doctor", "department", "date", "time"]
    list_per_page = 10
    ordering = ["-created_at"]


class PrescriptionModelAdmin(admin.ModelAdmin):
    list_display = [
        "appointment",
        "details",
        "created_at",
        "updated_at",
    ]
    list_filter = ["appointment"]
    search_fields = ["appointment"]
    list_per_page = 10
    ordering = ["-created_at"]
    date_hierarchy = 'created_at'


class RatingModelAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "appointment",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "patient",
        "doctor",
        "appointment",
    ]
    search_fields = ["appointment"]
    list_per_page = 10
    raw_id_fields = [
        "patient",
        "doctor",
        "appointment",
    ]
    ordering = ["-created_at"]


admin.site.register(AppointmentModel, AppointmentModelAdmin)
admin.site.register(PrescriptionModel, PrescriptionModelAdmin)
admin.site.register(RatingModel, RatingModelAdmin)
admin.site.register(PaymentModel)
