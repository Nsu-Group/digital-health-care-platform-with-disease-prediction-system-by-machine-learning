from django.db import models


class StoreModel(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	longitude = models.DecimalField(max_digits=12, decimal_places=8, default=0.0)
	latitude = models.DecimalField(max_digits=12, decimal_places=8, default=0.0)
	phone = models.CharField(max_length=100, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField()
	image = models.ImageField(upload_to="store_image", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Store"
		verbose_name_plural = "Stores"
