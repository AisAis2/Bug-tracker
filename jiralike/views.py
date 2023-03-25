from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateNewProject
from django.contrib.auth.decorators import login_required
from ticket.forms import createTicket
from ticket.views import create_ticket
from .models import Project
from ticket.models import Ticket
from jiralike.models import User
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
# Create your views here.
def index(response):
	return render(response, "jiralike/index.html")


	
def home(response):
	# print(response.user.type)
	return render(response, "jiralike/home.html",{"user":response.user})





def proj(response, id):
	if Project.objects.filter(id = id).exists():
		pj = get_object_or_404(Project,id = id)
	else:
		return HttpResponseRedirect('/home')
	if response.user.is_anonymous:
		msg = 'You are not authorized'
		return render(response, 'jiralike/index.html',{'msg':msg})
	if pj in response.user.project.all():
		
		if response.method == "POST":
			
			if response.POST.get("editProject1"):
				
				return HttpResponseRedirect('/edit/%s' % id)
				# return edit(response, id) passing response didnt really work,lol

			if response.POST.get('delete'):
				pj.delete()
				return HttpResponseRedirect("/home")
			if response.POST.get("save"):
				if len(response.POST.get("change"))>2:
					pj.description = response.POST.get("change")
					pj.save()
			elif response.POST.get("addTicket"):
				return HttpResponseRedirect(reverse("ticket:create_ticket"))
		return render(response,"jiralike/proj_view.html",{"proj":pj})
	else:
		return HttpResponseRedirect("/home")

def edit(response,id):
	print('response is:   ')
	print(response.POST)
	pj = Project.objects.get(id = id)
	if response.method == 'POST':
		print(response.POST)
		if response.POST.get('ssss'):
			print(len(response.POST['title']))
			if len(response.POST['title'])>0 and len(response.POST['description'])>0:
				
				pj.name =response.POST['title']
				pj.description =response.POST['description']
				pj.save()
				return HttpResponseRedirect('/%s' % id)
	return render(response, "jiralike/edit_project.html",{"pj":pj})


		



@login_required
def create(response):
	
	if response.method == "POST":
		form = CreateNewProject(response.POST)#contain information and mapping into values
		if form.is_valid():
			item =form.save(commit = False)
			item.user =response.user
			item.save()
			response.user.project.add(item)
			return HttpResponseRedirect("/%i" %item.id)
	else:
		form = CreateNewProject()

	return render(response,"jiralike/create.html",{"form":form})


def view(response):
	if response.user.is_anonymous:
		return HttpResponseRedirect('/login')
	else:
		pj = Project.objects.filter(user = response.user)
		return render(response, "jiralike/proj_list.html",{"pj":pj})





