from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
	rchoices = [
		('Submitter','Submitter'),
		('Manager','Manager'),
		('Developer','Developer'),
		('Admin', 'Admin'),
	]
	role = models.CharField(
		max_length=40,
		choices = rchoices,
		default = 'Submitter'
	)	


class Project(models.Model):
	name =  models.CharField(max_length=200, null = False)
	description = models.TextField(blank =True, null=True)
	user = models.ForeignKey(User, on_delete =models.CASCADE, null =True,related_name="project")
	def __str__(self):
		return self.name




