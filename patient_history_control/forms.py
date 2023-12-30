from django import forms

from user_control.constants import HISTORY_TYPE_CHOICES
from .models import HistoryModel


class AddEditHistoryForm(forms.ModelForm):
    type = forms.CharField(widget=forms.Select(choices=HISTORY_TYPE_CHOICES))
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
	
    class Meta:
        model = HistoryModel
        fields = ['type', 'description', 'image']
