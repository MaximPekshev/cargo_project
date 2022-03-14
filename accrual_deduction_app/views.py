from django.shortcuts import render
from django.contrib.auth.models import Group
from cargoapp.models import Vehicle, Driver
from .models import AccrualDeduction, ReasonOfDeduction, TYPE

import datetime

def show_accrual_deduction(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()

        if request.user in users_in_group_logist:

            if request.GET.get('month'):
                month = datetime.datetime.strptime(request.GET.get('month'), '%Y-%m')
            else:
                month = datetime.datetime.today()

            context = {
                'AccrualDeduction' : AccrualDeduction.objects.filter(date__month=(month.strftime('%m'))).order_by('vehicle'),
                'month': month.strftime('%Y-%m'),
            }

            return render(request, 'accrual_deduction_app/accrual_deduction_list.html', context)


def new_accrual_deduction(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()

        if request.user in users_in_group_logist:
            print(TYPE[0])
            context = {

                'vehicles': Vehicle.objects.filter(logist=request.user),
                'reasons': ReasonOfDeduction.objects.all(),
                'types' : TYPE,

            }

        return render(request, 'accrual_deduction_app/new_accrual_deduction.html', context)

