from django import forms
from .models import Ticket

class createTicket(forms.ModelForm):
	class Meta:
		model = Ticket
		exclude = ('submitter','proj')
		widgets = {
			'title': forms.TextInput(attrs={
				'class': 'input-group input-group-sm mb-3'
			}),
			'description': forms.Textarea(attrs={
				'class': 'form-control','rows': '3',
			}),
			'assignee': forms.Select(attrs={
				'class': 'form-select form-select-sm'
			}),
			# 'proj': forms.Select(attrs={
			# 	'class': 'form-select form-select-sm'
			# }),
			'priority': forms.Select(attrs={
				'class': 'form-select form-select-sm'
			}),
			'status': forms.Select(attrs={
				'class': 'form-select form-select-sm'
			}),
			
		}

		