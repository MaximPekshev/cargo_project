from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import TrailerInsurance, VehicleInsurance
from cargoapp.models import Vehicle
import datetime

def insurance_trac_insurance(request):

    if request.user.is_authenticated:

        users_in_group_insurance = Group.objects.get(name="Страховка").user_set.all()

        if request.user in users_in_group_insurance:
            insurance = []
            for vehicle in Vehicle.objects.all().order_by('release_date', 'consignment'):
                osago = VehicleInsurance.objects.filter(vehicle=vehicle, type=0, to_date__gte=datetime.datetime.now()).order_by('to_date').first()
                casco = VehicleInsurance.objects.filter(vehicle=vehicle, type=1, to_date__gte=datetime.datetime.now()).order_by('to_date').first()
                if osago or casco:
                    insurance.append([
                        vehicle,
                        osago,
                        casco,
                        ])
            context = {
                'insurance': insurance,
            }

            return render(request, 'insurance_app/trac_insurance.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def insurance_trailer_insurance(request):

    if request.user.is_authenticated:

        users_in_group_insurance = Group.objects.get(name="Страховка").user_set.all()

        if request.user in users_in_group_insurance:

            context = {
                'insurance' : TrailerInsurance.objects.all().order_by('trailer__release_date', 'trailer__consignment'),
            }

            return render(request, 'insurance_app/trailer_insurance.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')
