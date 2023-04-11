from django.db import models

from jiralike.models import Project, User
from simple_history.models import HistoricalRecords
# Create your models here.

class Ticket(models.Model):
	description = models.TextField(blank = True, null = True)
	slug = models.SlugField(default='slug')
	title = models.CharField(max_length=200, null=False, default='title')
	submitter = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
	assignee = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='tickets',null=True)
	proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, default = 1)
	pty = 	[
			('Lowest', 'Lowest'),
			('Low','Low'),
			('Medium','Medium'),
			('High', 'High'),
			('Highest','Highest'),
			]	
	sts =[
		('Open','Open'),
		('Done','Done'),
		('In Progress', 'In Progress'),
		]
	tps = [
		('Bugs/errors','Bugs/errors'),
		('Feature Requests','Feature Requests'),
		('Other Comments','Other Comments'),
	]
	priority = models.CharField(
		max_length=20,
		choices = pty,
		default = 'Lowest'
	)

	status = models.CharField(
		max_length=20,
		choices = sts,
		default = 'Open'
	)
	created = models.TimeField("Created", auto_now=False,auto_now_add=True)
	types = models.CharField(
		max_length = 30,
		choices = tps,
		default = 'Other Comments'
	)
	history = HistoricalRecords()
	class Meta:
		app_label = 'ticket'

	def __str__(self):
		return self.title
	def get_absoulte_url(self):
		return f'/{self.slug}/'