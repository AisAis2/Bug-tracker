from django import forms	
from .models import Project
from django.contrib.auth.models import User

class CreateNewProject(forms.ModelForm):
	class Meta:
		model = Project
		
		exclude = ('user',)