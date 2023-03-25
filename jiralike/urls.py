from django.urls import path

from . import views
# app_name = 'jiralike'
urlpatterns = [
path("",views.index, name = "index"),
path("home/",views.home, name = "home"),
path("create/",views.create, name = "create"),
path("<int:id>",views.proj, name = "proj"),
path("view/",views.view, name = "view"),
path("edit/<int:id>/", views.edit, name ='edit'),

]