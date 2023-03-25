from django.contrib import admin
from .models import  Project, User
from ticket.models import Ticket
# Register your models here.
# admin.site.register(Ticket)
admin.site.register(Project)
admin.site.register(User)
