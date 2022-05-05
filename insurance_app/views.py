from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import TrailerInsurance

def insurance_trac_insurance(request):

    if request.user.is_authenticated:

        users_in_group_insurance = Group.objects.get(name="Страховка").user_set.all()

        if request.user in users_in_group_insurance:

            context = {

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
