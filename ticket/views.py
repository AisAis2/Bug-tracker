from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  createTicket
from .models import Ticket
from jiralike.models import Project, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TicketSerializer
# Create your views here.
@permission_required('ticket.add_ticket', login_url='/home/')
def test(response,pk):
	pj = Project.objects.get(id = pk)
	form = createTicket(response.POST or None)
	if response.method == 'POST':
		form = createTicket(response.POST)
		if form.is_valid():
			tck = form.save(commit = False)
			tck.submitter = response.user
			tck.proj = pj
			tck.save()
			# return HttpResponseRedirect(reverse('ticket:tview'))
			return HttpResponseRedirect(reverse('proj', args = (tck.proj.id,)))
	return render(response, 'ticket/test.html',{
		"form":form,
	})



# @login_required
# def create_ticket(response):
# 	print('create')
# 	user = User.objects.all()
# 	pj = Project.objects.all()
# 	form = createTicket(response.POST or None)
# 	if response.method == 'POST':
# 		form = createTicket(response.POST)
# 		if form.is_valid():
# 			tck = form.save(commit = False)
# 			tck.proj = pj
# 			tck.save()
# 			return HttpResponseRedirect('/home')
# 	else:
# 		form = createTicket()
# 	return render(response, "ticket/create_ticket.html",{
#         "user":user,
        
#         })
@permission_required('ticket.change_ticket', login_url='/home/')
def edit_ticket(response,id):
	instance = get_object_or_404(Ticket,id = id)
	form = createTicket(response.POST or None, instance = instance)
	if response.method == 'POST':
		if response.POST.get("save"):
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse("ticket:tview"))
		if response.POST.get('delete'):
			instance.delete()
			return HttpResponseRedirect(reverse("ticket:tview"))
	return render(response,'ticket/edit_ticket.html',{"form":form,"user":response.user})


def ticket(response,id):
	ticket = Ticket.objects.get(id = id)
	return render(response,	"ticket/ticket.html",{"ticket":ticket})
@login_required
def tview(response):
	query = response.GET.get('query','')
	t = Ticket.objects.filter(assignee = response.user)
	if query:
		t = t.filter(Q(title__icontains = query) | Q(description__icontains = query)|Q(types__icontains = query))#cannot filter foreignkeys
	return render(response, "ticket/tickets_view.html",{
		"tickets":t,
		"query":query,
		})

def backlog(request):
	return render(request,"ticket/backlog.html",{
		"user":request.user,
	})


class TicketList(APIView):
	def get(self, request, format=None):
		tickets = Ticket.objects.all()[0:4]
		serializer = TicketSerializer(tickets, many=True) # many- more than one object
		return Response(serializer.data)
# class TicketInfo(APIView):
# 	def get_object(self, request):
