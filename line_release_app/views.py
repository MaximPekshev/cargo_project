from django.shortcuts import render, redirect
from .models import LineRelease
from cargoapp.models import Vehicle, Driver, Trailer
from django.contrib.auth.models import Group
from .forms import LineReleaseForm

def show_line_release_list(request):
    
    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        users_in_group = set(users_in_group_vehicle_supervisor | users_in_group_chief_column)

        if request.user in users_in_group:

            context ={
                'line_releases': LineRelease.objects.filter(columnar=request.user).reverse(),
            }

            return render(request, 'line_release_app/line_release_list.html', context)
        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')    


def line_release_add(request):
    
    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        users_in_group = set(users_in_group_vehicle_supervisor | users_in_group_chief_column)

        if request.user in users_in_group:
            
            if request.method == 'POST':

                line_release_form = LineReleaseForm(request.POST)

                if line_release_form.is_valid():

                    input_release_date = line_release_form.cleaned_data['input_release_date']
                    input_vehicle = line_release_form.cleaned_data['input_vehicle']
                    input_trailer = line_release_form.cleaned_data['input_trailer']
                    input_driver = line_release_form.cleaned_data['input_driver']
                    input_renewal = line_release_form.cleaned_data['input_renewal']
                    input_for_repair = line_release_form.cleaned_data['input_for_repair']
                    
                    new_line_release = LineRelease(
                        begin_date = input_release_date,
                        renewal = input_renewal,
                        for_repair = input_for_repair,
                        columnar = request.user,
                    )

                    try:
                        vehicle = Vehicle.objects.get(uid=input_vehicle)
                        new_line_release.vehicle = vehicle  
                    except:
                        pass  

                    try:
                        driver = Driver.objects.get(uid=input_driver)
                        new_line_release.driver = driver  
                    except:
                        pass

                    try:
                        trailer = Trailer.objects.get(uid=input_trailer)
                        new_line_release.trailer = trailer  
                    except:
                        pass

                    new_line_release.save()

            
            return redirect('show_line_release_list')

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def line_release_new(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        users_in_group = set(users_in_group_vehicle_supervisor | users_in_group_chief_column)

        if request.user in users_in_group:

            context = {
                'vehicles' : Vehicle.objects.filter(columnar=request.user),
                'drivers' : Driver.objects.all(),
                'trailers' : Trailer.objects.all(),
            }

            return render(request, 'line_release_app/line_release_new.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')    