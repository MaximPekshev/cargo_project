from django.urls import path

from .views import login, logout, authorisation_form

urlpatterns = [
	path('', 		authorisation_form , name='authorisation_form'),
	path('login/', 	login , name='login'),
	path('logout/', logout , name='logout'),
]