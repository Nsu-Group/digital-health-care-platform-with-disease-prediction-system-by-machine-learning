from django.db import models
from user_control.models import PatientModel


class HistoryModel(models.Model):
	user = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images/history/", null=True, blank=True)
	type= models.CharField(max_length=255)
	description = models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.type
