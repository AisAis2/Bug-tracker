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
from ticket.views import test
# Create your views here.
def index(response):
	return render(response, "jiralike/index.html")


	
def home(response):
	tck = Ticket.objects.all()

	bug_errors,feature_requests,other_comments =0,0,0
	lowest,low,medium,high,highest=0,0,0,0,0
	for t in tck:
		if t.types == 'Bugs/errors':
			bug_errors+=1
		elif t.types == 'Feature Requests':
			feature_requests+=1
		elif t.types == 'Other Comments':
			other_comments+=1
		s = t.priority
		if s =="Low":
			low+=1
		elif s == "Medium":
			medium+=1
		elif s=="High":
			high+=1
		elif s=="Highest":
			highest+=1	
		else:
			lowest+=1
	data_points =[
		{"label":"Bugs/errors","y":bug_errors},
		{"label":'Feature Requests',"y":feature_requests},
		{"label":'Other Comments',"y":other_comments},
	]
	data_points2 =[
		{"label":"Lowest","y":lowest},
		{"label":'Low',"y":low},
		{"label":'Medium',"y":medium},
		{"label":'High',"y":high},
		{"label":'Highest',"y":highest},
	]
	dp=[]
	dp.append(data_points)
	dp.append(data_points2)
	return render(response, "jiralike/home.html",{"user":response.user, "data_points":dp})





def proj(response, id):
	pj = get_object_or_404(Project,id = id)
	if response.user.is_anonymous:
		msg = 'You are not authorized'
		return render(response, 'jiralike/index.html',{'msg':msg})
	if response.method == "POST":
		if response.POST.get("editProject1"):
			return HttpResponseRedirect('/edit/%s' % id)
			# return edit(response, id) passing response didnt really work,lol
		if response.POST.get('delete') and pj.user == response.user:
			pj.delete()
			return HttpResponseRedirect("/home")
		else:
			msg = 'You are not authorized to delete this project.'
			return render(response, 'jiralike/index.html',{'msg':msg})
	# if response.GET.get("addTicket",''):
	# 	return HttpResponseRedirect(reverse("ticket"))
	return render(response,"jiralike/proj_view.html",{"proj":pj})


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
@permission_required("jiralike.add_project")
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
		tcks = Ticket.objects.filter(assignee = response.user)
		
		return render(response, "jiralike/proj_list.html",{
			"pj":pj,
			'tcks':tcks,
			})





