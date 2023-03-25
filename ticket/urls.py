from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [ 
path('<int:id>/',views.ticket, name='ticket'),
path("tview/", views.tview, name ='tview'),
path("create_ticket/",views.test, name = "create_ticket"),
path("edit/<int:id>/", views.edit_ticket, name ='edit'),
path('test/', views.test, name ='test')

]