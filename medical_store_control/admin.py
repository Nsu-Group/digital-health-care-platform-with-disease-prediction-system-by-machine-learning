from django.contrib import admin

from .models import *

class StoreModelAdmin(admin.ModelAdmin):
	list_display = (
		"name",
		"description",
		"phone",
		"address",
		"created_at",
	)
	search_fields = (
		"user",
		"name",
	)
	readonly_fields = (
		"created_at",
		"updated_at",
	)
	list_per_page = 30
	ordering = ("created_at",)

admin.site.register(StoreModel, StoreModelAdmin)
