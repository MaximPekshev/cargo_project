from django.shortcuts import render, redirect
from .models import ServiceWorkType, ServiceOrganization, ServiceWork, ServiceWorkStatus
from cargoapp.models import Vehicle
from .forms import ScheduledRepairForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
import datetime

def show_scheduled_repair_list(request):

    if request.user.is_authenticated:

        context = {
            'service_work_list': ServiceWork.objects.all(),
        }

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()
        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        
        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column):

            return render(request, 'scheduled_repair_app/scheduled_repair_list.html', context)

        if request.user in set(users_in_group_logistsupervisor | users_in_group_logist):

            return render(request, 'scheduled_repair_app/scheduled_repair_list_logist.html', context)

    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')    


def scheduled_repair_new(request):

    if request.user.is_authenticated:

        context = {
            'service_work_type': ServiceWorkType.objects.all(),
            'vehicles': Vehicle.objects.all(),
            'sto': ServiceOrganization.objects.all(),
        }

        return render(request, 'scheduled_repair_app/scheduled_repair_new.html', context)

    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')    

def scheduled_repair_add(request):

    if request.user.is_authenticated:
        
        if request.method == 'POST':

            service_work_form = ScheduledRepairForm(request.POST, request.FILES)

            if service_work_form.is_valid():

                service_work_type_uid = service_work_form.cleaned_data['service_work_type']
                vehicle_uid = service_work_form.cleaned_data['vehicle']
                title = service_work_form.cleaned_data['title']
                date_from = service_work_form.cleaned_data['date_from']
                date_to = service_work_form.cleaned_data['date_to']
                sto_uid = service_work_form.cleaned_data['sto']
                comment = service_work_form.cleaned_data['comment']

                new_service_work = ServiceWork()

                new_service_work.from_date = date_from
                new_service_work.to_date = date_to
                new_service_work.title = title
                new_service_work.comment = comment
                new_service_work.autor = request.user

                try:
                    service_work_type = ServiceWorkType.objects.get(uid=service_work_type_uid)
                    new_service_work.type = service_work_type
                except:
                    pass

                try:
                    vehicle = Vehicle.objects.get(uid=vehicle_uid)
                    new_service_work.vehicle = vehicle
                except:
                    pass

                try:
                    sto = ServiceOrganization.objects.get(uid=sto_uid)
                    new_service_work.service_organization = sto
                except:
                    pass
                
                try:
                    status = ServiceWorkStatus.objects.get(title='Запланировано')
                except:
                    status = ServiceWorkStatus(title='Запланировано')
                    status.save()
                new_service_work.status = status


                new_service_work.save()

                context = {
                    'service_work_list': ServiceWork.objects.all(),
                }

                return redirect('show_scheduled_repair_list')
    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')            

def scheduled_repair_save(request, pk):

    if request.user.is_authenticated:
        
        service_work_object = get_object_or_404(ServiceWork, pk=pk)

        if request.method == 'POST':

            service_work_form = ScheduledRepairForm(request.POST, request.FILES)

            if service_work_form.is_valid():

                users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
                users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
                users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()
                users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
                
                if request.user in set(users_in_group_logistsupervisor | users_in_group_logist):

                    date_from_logist = service_work_form.cleaned_data['date_from_logist']
                    comment = service_work_form.cleaned_data['comment']
                    status_uid= service_work_form.cleaned_data['status']

                    service_work_object.comment = comment
                    service_work_object.from_date_logist = date_from_logist

                    try:
                        service_work_status = ServiceWorkStatus.objects.get(uid=status_uid)
                        service_work_object.status = service_work_status
                    except:
                        pass

                if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column):

                    service_work_type_uid = service_work_form.cleaned_data['service_work_type']
                    vehicle_uid = service_work_form.cleaned_data['vehicle']
                    title = service_work_form.cleaned_data['title']
                    date_from = service_work_form.cleaned_data['date_from']
                    date_to = service_work_form.cleaned_data['date_to']
                    sto_uid = service_work_form.cleaned_data['sto']
                    comment = service_work_form.cleaned_data['comment']
                    status_uid= service_work_form.cleaned_data['status']

                    service_work_object.from_date = date_from
                    service_work_object.to_date = date_to
                    service_work_object.title = title
                    service_work_object.comment = comment
                    
                    try:
                        service_work_type = ServiceWorkType.objects.get(uid=service_work_type_uid)
                        service_work_object.type = service_work_type
                    except:
                        pass

                    try:
                        vehicle = Vehicle.objects.get(uid=vehicle_uid)
                        service_work_object.vehicle = vehicle
                    except:
                        pass

                    try:
                        sto = ServiceOrganization.objects.get(uid=sto_uid)
                        service_work_object.service_organization = sto
                    except:
                        pass

                    try:
                        service_work_status = ServiceWorkStatus.objects.get(uid=status_uid)
                        service_work_object.status = service_work_status
                    except:
                        pass

                service_work_object.save()

                return redirect('scheduled_repair_object', pk=service_work_object.pk)
    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')   

def scheduled_repair_object(request, pk):

    if request.user.is_authenticated:

        service_work_object = get_object_or_404(ServiceWork, pk=pk)

        context = {
            'service_work_object': service_work_object,
            'service_work_type': ServiceWorkType.objects.all().exclude(uid=service_work_object.type.uid),
            'vehicles': Vehicle.objects.all().exclude(uid=service_work_object.vehicle.uid),
            'sto': ServiceOrganization.objects.all().exclude(uid=service_work_object.service_organization.uid),
            'statuses': ServiceWorkStatus.objects.all().exclude(uid=service_work_object.status.uid)
        }

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="Начальник колонных").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()
        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()
        
        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column):

            return render(request, 'scheduled_repair_app/scheduled_repair_object.html', context)

        if request.user in set(users_in_group_logistsupervisor | users_in_group_logist):

            return render(request, 'scheduled_repair_app/scheduled_repair_object_logist.html', context)    

    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')

def show_scheduled_plan_fact_vehicle_list(request):

    if request.user.is_authenticated:

        year = datetime.datetime.now().strftime('%Y')

        context = {
            'service_work_list': ServiceWork.objects.filter(from_date_logist__year=year),
        }

        return render(request, 'scheduled_repair_app/plan_fact/schedule_auto.html', context)

    else:

        return render(request, 'cargoapp/menu/auth_role_error.html')    