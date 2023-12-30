from django.urls import path

from .views import *

urlpatterns = [
	path("", home_view, name="medical-store-home"),
	path("store/<int:id>/", store_detail_view, name="store-detail"),
]
