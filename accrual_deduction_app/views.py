from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from cargoapp.models import Vehicle, Driver
from .models import AccrualDeduction, ReasonOfDeduction, TYPE
from .forms import AccrualDeductionForm
from decimal import Decimal

from django.shortcuts import get_object_or_404

import datetime

def accrual_deduction_list(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()

        if request.user in users_in_group_logist or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            if request.GET.get('month'):
                month = datetime.datetime.strptime(request.GET.get('month'), '%Y-%m')
            else:
                month = datetime.datetime.today()

            context = {
                'AccrualDeduction' : AccrualDeduction.objects.filter(date__month=(month.strftime('%m'))).order_by('vehicle'),
                'month': month.strftime('%Y-%m'),
            }

            return render(request, 'accrual_deduction_app/accrual_deduction_list.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def new_accrual_deduction(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()

        if request.user in users_in_group_logist or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:
            context = {

                'reasons': ReasonOfDeduction.objects.all(),
                'types' : TYPE,

            }
            if request.user in users_in_group_logist:
                context.update({'vehicles': Vehicle.objects.filter(logist=request.user)})
            if request.user in users_in_group_vehicle_supervisor:
                context.update({'vehicles': Vehicle.objects.filter(columnar=request.user)})
            if request.user in users_in_group_chief_column:
                context.update({'vehicles': Vehicle.objects.all()})

            return render(request, 'accrual_deduction_app/new_accrual_deduction.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')    


def show_accrual_deduction(request, uid):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()

        if request.user in users_in_group_logist or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:
            
            accrual_deduction = get_object_or_404(AccrualDeduction, uid=uid)

            context = {

                'reasons': ReasonOfDeduction.objects.all().exclude(id=accrual_deduction.reason.id),
                'types' : TYPE,
                'accrual_deduction' : accrual_deduction,
                
            }

            if request.user in users_in_group_logist:
                context.update({'vehicles': Vehicle.objects.filter(logist=request.user).exclude(uid=accrual_deduction.vehicle.uid)})
            if request.user in users_in_group_vehicle_supervisor:
                context.update({'vehicles': Vehicle.objects.filter(columnar=request.user).exclude(uid=accrual_deduction.vehicle.uid)})
            if request.user in users_in_group_chief_column:
                context.update({'vehicles': Vehicle.objects.all().exclude(uid=accrual_deduction.vehicle.uid)})    

            return render(request, 'accrual_deduction_app/accrual_deduction.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')    

def add_accrual_deduction(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        
        if request.user in users_in_group_logist or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            if request.method == 'POST':

                accrual_form = AccrualDeductionForm(request.POST)

                if accrual_form.is_valid():

                    date = accrual_form.cleaned_data['input_date']
                    sum = accrual_form.cleaned_data['input_sum']
                    vehicle_uid = accrual_form.cleaned_data['input_vehicle']
                    reason_id = accrual_form.cleaned_data['input_reason']
                    type = accrual_form.cleaned_data['input_type']

                    try:
                        vehicle = Vehicle.objects.get(uid=vehicle_uid)
                    except:
                        vehicle = None

                    try:
                        reason = ReasonOfDeduction.objects.get(id=reason_id)
                    except:
                        reason = None    

                    new_accrual = AccrualDeduction(
                        date=date,
                        sum=sum,
                        vehicle=vehicle,
                        driver=vehicle.driver,
                        logist=request.user,
                        reason=reason,
                        type=type,
                    )

                    new_accrual.save()

                    # month = datetime.datetime.today()

                    # context = {

                    #     'AccrualDeduction' : AccrualDeduction.objects.filter(date__month=(month.strftime('%m'))).order_by('vehicle'),
                    #     'month': month.strftime('%Y-%m'),

                    # }

                    return redirect('show_accrual_deduction', uid=new_accrual.uid)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')            



def save_accrual_deduction(request,uid):

     if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        
        if request.user in users_in_group_logist or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            accrual_deduction = get_object_or_404(AccrualDeduction, uid=uid)

            if request.method == 'POST':

                accrual_form = AccrualDeductionForm(request.POST)

                if accrual_form.is_valid():

                    date = accrual_form.cleaned_data['input_date']
                    sum = accrual_form.cleaned_data['input_sum']
                    vehicle_uid = accrual_form.cleaned_data['input_vehicle']
                    reason_id = accrual_form.cleaned_data['input_reason']
                    type = accrual_form.cleaned_data['input_type']

                    try:
                        vehicle = Vehicle.objects.get(uid=vehicle_uid)
                    except:
                        vehicle = None

                    try:
                        reason = ReasonOfDeduction.objects.get(id=reason_id)
                    except:
                        reason = None

                    if vehicle and reason:

                        accrual_deduction.date = date
                        accrual_deduction.sum = Decimal(sum.replace(',','.'))
                        accrual_deduction.vehicle = vehicle
                        accrual_deduction.reason = reason
                        accrual_deduction.driver = vehicle.driver
                        accrual_deduction.type = type

                        accrual_deduction.save()

                        return redirect('show_accrual_deduction', uid=accrual_deduction.uid)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')                