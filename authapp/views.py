from django.shortcuts import render, redirect

from django.contrib		 			import auth
from cargoapp.models				import LogistUser
from django.contrib.auth.forms 		import AuthenticationForm
from django.contrib					import messages
from django.contrib.auth.models 	import Group

def authorisation_form(request):
	return render(request, 'authapp/auth.html')

def login(request):

	if request.method == 'POST':

		form 				= AuthenticationForm(request, request.POST)

		username 		= form.data.get('username')
		password 		= form.data.get('password')

		user 			= auth.authenticate(username=username, password=password)

		if user:

			auth.login(request, user)
			
			return redirect('show_index_page')

		else:

			messages.info(request, 'Комбинации пароль-логин не существует! Обратитесь к администратору!')

			return redirect('authorisation_form')
	
	return redirect('authorisation_form')


def logout(request):

	auth.logout(request)

	return redirect('authorisation_form')