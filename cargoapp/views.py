from calendar import month
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from .models import Vehicle
from .serializers import VehicleSerializer
from .models import Vehicle_status
from .models import Route
from .serializers import RouteSerializer
from .models import LogistUser
from .serializers import LogistUserSerializer
from .models import City
from .serializers import CitySerializer
from .models import Organization
from .serializers import OrganizationSerializer
from .models import Contracts
from .serializers import ContractsSerializer
from .models import Constant
from django.contrib	import auth

from autographapp.models import AutographDailyIndicators

from django.contrib.auth.models import Group

from autographapp.models import AutographDailyIndicators
from .models import MileageRevenueStandard
import datetime


from django.db.models import Sum
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions

from .forms import RouteForm, FilterForm
from django.contrib import messages
from decimal import Decimal

import googlemaps
import json
import re
from decouple import config

from django.db.models import Q

import folium

class CityList(generics.ListAPIView):
    
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.all()

class ContractsList(generics.ListCreateAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContractFilterdList(generics.ListAPIView):
    
    serializer_class = ContractsSerializer

    def get_queryset(self):

        contragent_uid = self.kwargs['uid']
        return Contracts.objects.filter(contragent__uid=contragent_uid)

class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DriverList(generics.ListCreateAPIView):
	queryset = Driver.objects.all()
	serializer_class = DriverSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LogistUserList(generics.ListCreateAPIView):
    queryset = LogistUser.objects.all()
    serializer_class = LogistUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RouteList(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

class LogistUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LogistUser.objects.all()
    serializer_class = LogistUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class ContractsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'    

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class RouteDetail(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class DriverDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'


def show_menu_page(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_fuel_dep = Group.objects.get(name="?????????????????? ??????????").user_set.all()
        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()
        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_hr_dep = Group.objects.get(name="?????????? ????????????").user_set.all()
        users_in_group_insurance = Group.objects.get(name="??????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_hr_director = Group.objects.get(name="???????????????? ???? ??????????????????").user_set.all()
        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()

        if request.user in users_in_group_hr_director:
            
            return render(request, 'cargoapp/menu/hr_director_menu.html')

        elif request.user in users_in_group_logistsupervisor:

            return render(request, 'cargoapp/menu/supervisor_menu.html')

        elif request.user in users_in_group_driver:
             
            return render(request, 'cargoapp/menu/driver_menu.html')

        elif request.user in users_in_group_fuel_dep:
             
            return render(request, 'cargoapp/menu/fuel_dep_menu.html')    

        elif request.user in users_in_group_logist:

            return render(request, 'cargoapp/menu/logist_menu.html')

        elif request.user in users_in_group_vorotny:

            return render(request, 'cargoapp/menu/vorotny_menu.html')

        elif request.user in users_in_group_hr_dep:

            return render(request, 'cargoapp/menu/hr_department.html')

        elif request.user in users_in_group_insurance:

            return render(request, 'cargoapp/menu/insurance_menu.html')

        # ?????????? ?????????????????? ???????? ?????? ???????????????? ?? ?????????????????????? ????????????????
        elif request.user in users_in_group_chief_column or request.user in users_in_group_vehicle_supervisor:

            users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()
            users_in_group_logist = Group.objects.get(name="????????????").user_set.all()
            users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
            users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()

            columnars = users_in_group_vehicle_supervisor
            vehicle_statuses = Vehicle_status.objects.all()

            map = folium.Map(
                location = [64.6863136, 97.7453061],
                zoom_start = 4
            )
            vehicles_list = Vehicle.objects.all()

            context = {}

            filterForm = FilterForm(request.GET)
            
            if filterForm.is_valid():

                user_uid = filterForm.cleaned_data['user_uid']
                input_status = filterForm.cleaned_data['status']

                if user_uid:

                    try:
                        user_object = LogistUser.objects.get(uid=user_uid) 
                    except:
                        user_object = None

                    if user_object:

                        context.update({'actual_user' : user_object,})

                        if user_object in users_in_group_vehicle_supervisor:

                            vehicles_list = vehicles_list.filter(columnar=user_object)
                            columnars = columnars.exclude(username=user_object.username)


                        if user_object in users_in_group_logist:

                            vehicles_list = vehicles_list.filter(logist=user_object)
                            users_in_group_logist = users_in_group_logist.exclude(username=user_object.username)


                        if user_object in users_in_group_logistsupervisor:

                            vehicles_list = vehicles_list.filter(logist__in=LogistUser.objects.filter(supervisor=user_object))
                            users_in_group_logistsupervisor = users_in_group_logistsupervisor.exclude(username=user_object.username)

                        if user_object in users_in_group_chief_column:

                            users_in_group_logistsupervisor = users_in_group_logistsupervisor.exclude(username=user_object.username)           
                    
                if input_status:
                    
                    try:
                        status_object = Vehicle_status.objects.get(title=input_status)
                        vehicles_list = vehicles_list.filter(status=status_object)
                        vehicle_statuses = vehicle_statuses.exclude(title=status_object.title)
                        context.update({'actual_status' : status_object,})
                    except:
                        pass    


            for vehicle in vehicles_list:

                last_autograph_day = AutographDailyIndicators.objects.filter(vehicle=vehicle).order_by('date').last()
                if last_autograph_day:
                    folium.Marker(
                        [last_autograph_day.last_lat, last_autograph_day.last_lng], 
                        icon=folium.DivIcon(html=f"""<div class="map-label" style="font-family: courier new; color: { vehicle.status.color }"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
                        <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                        <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                        </svg><i>{vehicle.car_number.replace(" ", "")}</i></div>""")
                    ).add_to(map)

            map = map._repr_html_()

            context.update({
                'map' : map,
                'vehicles_list': vehicles_list,
                'logist_sv': users_in_group_logistsupervisor,
                'logists': users_in_group_logist,
                'chief_columns': users_in_group_chief_column,
                'columnars': columnars,
                'statuses': vehicle_statuses,
            })

            if request.user in users_in_group_vehicle_supervisor:

                return render(request, 'cargoapp/menu/chief_column_menu.html', context)

            elif request.user in users_in_group_chief_column:

                return render(request, 'cargoapp/menu/chief_column_menu.html', context)

        elif request.user in users_in_group_health_safety:

            return render(request, 'cargoapp/menu/health_safety.html')        

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')
    else:

        return redirect('login') 

def repair_request_menu(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()
        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_logistsupervisor | users_in_group_logist | users_in_group_chief_column):
            return render(request, 'cargoapp/repair_request/menu.html')
        else:
            return render(request, 'cargoapp/menu/auth_role_error.html')
    else:

        return redirect('login')

def show_driver_list(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column):

            if request.user in users_in_group_vehicle_supervisor:
                vehicles = Vehicle.objects.filter(columnar=request.user).order_by('driver__title')

            elif request.user in users_in_group_chief_column:
                vehicles = Vehicle.objects.filter(columnar__in=LogistUser.objects.filter(supervisor=request.user)).order_by('driver__title')

            context = {
                'vehicles' : vehicles,
            }

            return render(request, 'cargoapp/driver_list.html', context)
        else:
            return render(request, 'cargoapp/menu/auth_role_error.html')
    else:

        return redirect('login')

def show_vehicle_list(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column):

            if request.user in users_in_group_vehicle_supervisor:
                vehicles = Vehicle.objects.filter(columnar=request.user).order_by('driver__title')

            elif request.user in users_in_group_chief_column:
                vehicles = Vehicle.objects.filter(columnar__in=LogistUser.objects.filter(supervisor=request.user)).order_by('driver__title')

            context = {
                'vehicles' : vehicles,
            }

            return render(request, 'cargoapp/vehicle_list.html', context)
        else:
            return render(request, 'cargoapp/menu/auth_role_error.html')
    else:

        return redirect('login')        


def get_planned_data(vehicles, month):

    mileageStandard = 0
    revenueStandard = 0
    net_incomeStandart = 0

    for vehicle in vehicles:
        milageStandart = MileageRevenueStandard.objects.filter(vehicle=vehicle, date__lte=month).order_by('-date').first()
        if milageStandart:
            mileageStandard += milageStandart.mileage
            revenueStandard += milageStandart.revenue
            net_incomeStandart += milageStandart.net_income

    return [mileageStandard, revenueStandard, net_incomeStandart]


def show_index_page(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()
        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor:
            if request.GET.get('date'):
                date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
            else:    
                date = datetime.datetime.now() -  datetime.timedelta(days=1)

            context = {
                'vehicles' : AutographDailyIndicators.objects.filter(date=date.date(), vehicle__in=Vehicle.objects.filter(columnar=request.user)),
                'date' : date.strftime("%Y-%m-%d"),
            }
            return render(request, 'autographapp/autograph.html', context)

        elif request.user in users_in_group_logistsupervisor:

            if request.GET.get('month'):
                month = datetime.datetime.strptime(request.GET.get('month'), '%Y-%m')
            else:
                month = datetime.datetime.today()

            logists  = LogistUser.objects.filter(supervisor=request.user)
            vehicle = None
            logist = None

            if request.GET.get('vehicle') and not request.GET.get('logist'):
                vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
                routes = Route.objects.filter(vehicle=vehicle).order_by('logist', '-from_date')
                planned_data = get_planned_data([vehicle], month)

            elif not request.GET.get('vehicle') and request.GET.get('logist'):
                logist = LogistUser.objects.get(uid=request.GET.get('logist'))
                routes = Route.objects.filter(logist=logist).order_by('logist', '-from_date')
                planned_data = get_planned_data(Vehicle.objects.filter(logist=logist), month)

            elif request.GET.get('vehicle') and request.GET.get('logist'):
                vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
                logist = LogistUser.objects.get(uid=request.GET.get('logist'))
                routes = Route.objects.filter(logist=logist, vehicle=vehicle).order_by('logist', '-from_date')
                planned_data = get_planned_data([vehicle], month)

            else:
                routes = Route.objects.filter(logist__in=logists).order_by('logist', '-from_date')
                vehicle = None
                planned_data = get_planned_data(Vehicle.objects.filter(logist__in=logists), month)

            mileageStandard = planned_data[0]
            revenueStandard = planned_data[1]
            net_incomeStandart = planned_data[2]

            if vehicle:
                vehicles = Vehicle.objects.filter(logist__in=logists).exclude(uid=vehicle.uid)
            else:
                vehicles = Vehicle.objects.filter(logist__in=logists)

            if logist:
                logists =  LogistUser.objects.filter(supervisor=request.user).exclude(uid=logist.uid)
                vehicles = Vehicle.objects.filter(logist=logist)
            else:
                logists = LogistUser.objects.filter(supervisor=request.user)   

            routes  = routes.filter(Q(from_date__month=(month.strftime('%m'))) | Q(to_date__month=(month.strftime('%m'))))

            try:
                # total_routes_length = routes.aggregate(Sum('route_length'))['route_length__sum']
                total_cost_of_km = ((routes.aggregate(Sum('route_cost'))['route_cost__sum']/routes.aggregate(Sum('route_length'))['route_length__sum']).quantize(Decimal("1.00")))
            except:
                total_cost_of_km = Decimal(0)
                total_cost_of_km = total_cost_of_km.quantize(Decimal("1.00")) 

            plan_total_cost_of_km = Constant.objects.filter(title="?????????????????? ??????????????????", date__lte=datetime.datetime.now()).order_by('date').last().value
            if not plan_total_cost_of_km:
                plan_total_cost_of_km = Decimal(50).quantize(Decimal("1.00"))

            #?????????????????????? ????????????
            total_route_length = routes.aggregate(Sum('route_length'))['route_length__sum'].quantize(Decimal("1.00")) if routes else 0
            total_route_cost = routes.aggregate(Sum('route_cost'))['route_cost__sum'].quantize(Decimal("1.00")) if routes else 0
            total_pure_income = routes.aggregate(Sum('straight'))['straight__sum'].quantize(Decimal("1.00"))if routes else 0

            #???????????? ???????????????? ????????????????
            plan_total_route_length = Decimal(mileageStandard).quantize(Decimal("1.00"))
            plan_total_route_cost = Decimal(revenueStandard).quantize(Decimal("1.00"))
            plan_total_pure_income = Decimal(net_incomeStandart).quantize(Decimal("1.00"))

            #???????????? ???????????????? ???? ??????????
            route_length_diff = plan_total_route_length - total_route_length
            route_cost_diff = plan_total_route_cost - total_route_cost
            cost_of_km_diff = plan_total_cost_of_km - total_cost_of_km
            pure_income_diff = plan_total_pure_income - total_pure_income

            #???????????? ???????????????? ????????????????????
            try:
                route_length_percent = (total_route_length/plan_total_route_length*100).quantize(Decimal("1"))
            except:
                route_length_percent = Decimal(0).quantize(Decimal("1"))

            try:
                route_cost_percent = (total_route_cost/plan_total_route_cost*100).quantize(Decimal("1"))
            except:
                route_cost_percent = Decimal(0).quantize(Decimal("1"))

            try:
                cost_of_km_percent = (total_cost_of_km/plan_total_cost_of_km*100).quantize(Decimal("1"))
            except:
                cost_of_km_percent = Decimal(0).quantize(Decimal("1"))

            try:
                pure_income_percent = (total_pure_income/plan_total_pure_income*100).quantize(Decimal("1"))
            except:
                pure_income_percent = Decimal(0).quantize(Decimal("1")) 

            context = {
                'user' : request.user,
                'routes' : routes,
                'vehicles' : vehicles,
                'logists' : logists,
                'checked_vehicle': vehicle,
                'checked_logist': logist,
                'actual_month': month.strftime('%Y-%m'),
                'total_expenses_1' : routes.aggregate(Sum('expenses_1'))['expenses_1__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_route_cost' : total_route_cost,
                'total_route_length' : total_route_length,
                'total_days' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_fuel_cost' : routes.aggregate(Sum('fuel_cost'))['fuel_cost__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pay_check' : routes.aggregate(Sum('pay_check'))['pay_check__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pure_income' : total_pure_income,
                'total_cost_of_km' : total_cost_of_km,
                'total_cost_of_platon' : routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum'].quantize(Decimal("1.00")) if routes else 0 if routes else 0,
                'total_day_count' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,
                
                # 'plan_total_route_length' : mileageRevenueStandard.aggregate(Sum('mileage'))['milage__sum'].quantize(Decimal("1.00")) if mileageRevenueStandard else 0,
                'plan_total_route_length' : plan_total_route_length,
                'plan_total_route_cost' : plan_total_route_cost,
                'plan_total_cost_of_km' : plan_total_cost_of_km,
                'plan_total_pure_income' : plan_total_pure_income,

                'route_length_diff' : route_length_diff,
                'route_cost_diff' : route_cost_diff,
                'cost_of_km_diff' : cost_of_km_diff,
                'pure_income_diff' : pure_income_diff,

                'route_length_percent' : route_length_percent,
                'route_cost_percent' : route_cost_percent,
                'cost_of_km_percent' : cost_of_km_percent,
                'pure_income_percent' : pure_income_percent,
            }

            return render(request, 'cargoapp/supervisor_index.html', context)

        elif request.user in users_in_group_logist:
            if request.GET.get('month'):
                month = datetime.datetime.strptime(request.GET.get('month'), '%Y-%m')
            else:
                month = datetime.datetime.today()
            mileageStandard = 0
            revenueStandard = 0
            net_incomeStandart = 0

            if request.GET.get('vehicle'):
                vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
                routes = Route.objects.filter(logist=request.user, vehicle=vehicle).order_by('-from_date')
                milageStandart = MileageRevenueStandard.objects.filter(vehicle=vehicle, date__lte=month).order_by('-date').first()
                if milageStandart:
                    mileageStandard += milageStandart.mileage
                    revenueStandard += milageStandart.revenue
                    net_incomeStandart += milageStandart.net_income
            else:
                routes = Route.objects.filter(logist=request.user).order_by('-from_date')
                vehicle = None 
                for veh in Vehicle.objects.filter(logist=request.user):
                    milageStandart = MileageRevenueStandard.objects.filter(vehicle=veh, date__lte=month).order_by('-date').first()
                    if milageStandart:
                        mileageStandard += milageStandart.mileage
                        revenueStandard += milageStandart.revenue
                        net_incomeStandart += milageStandart.net_income

            routes  = routes.filter(Q(from_date__month=(month.strftime('%m'))) | Q(to_date__month=(month.strftime('%m'))))

            try:
                # total_routes_length = routes.aggregate(Sum('route_length'))['route_length__sum']
                total_cost_of_km = ((routes.aggregate(Sum('route_cost'))['route_cost__sum']/routes.aggregate(Sum('route_length'))['route_length__sum']).quantize(Decimal("1.00")))
            except:
                total_cost_of_km = Decimal(0)
                total_cost_of_km = total_cost_of_km.quantize(Decimal("1.00"))  

            # try:
            #     plan_total_cost_of_km = Decimal(revenueStandard/mileageStandard).quantize(Decimal("1.00"))
            # except:        
            #     plan_total_cost_of_km = Decimal(0).quantize(Decimal("1.00"))
            plan_total_cost_of_km = Constant.objects.filter(title="?????????????????? ??????????????????", date__lte=datetime.datetime.now()).order_by('date').last().value
            if not plan_total_cost_of_km:
                plan_total_cost_of_km = Decimal(50).quantize(Decimal("1.00"))

            #?????????????????????? ????????????
            total_route_length = routes.aggregate(Sum('route_length'))['route_length__sum'].quantize(Decimal("1.00")) if routes else 0
            total_route_cost = routes.aggregate(Sum('route_cost'))['route_cost__sum'].quantize(Decimal("1.00")) if routes else 0
            total_pure_income = routes.aggregate(Sum('straight'))['straight__sum'].quantize(Decimal("1.00"))if routes else 0

            #???????????? ???????????????? ????????????????
            plan_total_route_length = Decimal(mileageStandard).quantize(Decimal("1.00"))
            plan_total_route_cost = Decimal(revenueStandard).quantize(Decimal("1.00"))
            plan_total_pure_income = Decimal(net_incomeStandart).quantize(Decimal("1.00"))

            #???????????? ???????????????? ???? ??????????
            route_length_diff = plan_total_route_length - total_route_length
            route_cost_diff = plan_total_route_cost - total_route_cost
            cost_of_km_diff = plan_total_cost_of_km - total_cost_of_km
            pure_income_diff = plan_total_pure_income - total_pure_income

            #???????????? ???????????????? ????????????????????
            try:
                route_length_percent = (total_route_length/plan_total_route_length*100).quantize(Decimal("1"))
            except:
                route_length_percent = Decimal(0).quantize(Decimal("1"))

            try:
                route_cost_percent = (total_route_cost/plan_total_route_cost*100).quantize(Decimal("1"))
            except:
                route_cost_percent = Decimal(0).quantize(Decimal("1"))

            try:
                cost_of_km_percent = (total_cost_of_km/plan_total_cost_of_km*100).quantize(Decimal("1"))
            except:
                cost_of_km_percent = Decimal(0).quantize(Decimal("1"))

            try:
                pure_income_percent = (total_pure_income/plan_total_pure_income*100).quantize(Decimal("1"))
            except:
                pure_income_percent = Decimal(0).quantize(Decimal("1"))       

            context = {
                'user' : request.user,
                'routes' : routes,
                'vehicles' : Vehicle.objects.filter(logist=request.user),
                'checked_vehicle' : vehicle,
                'actual_vehicle': vehicle,
                'actual_month': month.strftime('%Y-%m'),
                'total_expenses_1' : routes.aggregate(Sum('expenses_1'))['expenses_1__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_route_cost' : total_route_cost,
                'total_route_length' : total_route_length,
                'total_days' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_fuel_cost' : routes.aggregate(Sum('fuel_cost'))['fuel_cost__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pay_check' : routes.aggregate(Sum('pay_check'))['pay_check__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pure_income' : total_pure_income,
                'total_cost_of_km' : total_cost_of_km,
                'total_cost_of_platon' : routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum'].quantize(Decimal("1.00")) if routes else 0 if routes else 0,
                'total_day_count' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,

                # 'plan_total_route_length' : mileageRevenueStandard.aggregate(Sum('mileage'))['milage__sum'].quantize(Decimal("1.00")) if mileageRevenueStandard else 0,
                'plan_total_route_length' : plan_total_route_length,
                'plan_total_route_cost' : plan_total_route_cost,
                'plan_total_cost_of_km' : plan_total_cost_of_km,
                'plan_total_pure_income' : plan_total_pure_income,

                'route_length_diff' : route_length_diff,
                'route_cost_diff' : route_cost_diff,
                'cost_of_km_diff' : cost_of_km_diff,
                'pure_income_diff' : pure_income_diff,

                'route_length_percent' : route_length_percent,
                'route_cost_percent' : route_cost_percent,
                'cost_of_km_percent' : cost_of_km_percent,
                'pure_income_percent' : pure_income_percent,
            }

            return render(request, 'cargoapp/logist_index_page.html', context)

        elif request.user in users_in_group_chief_column:

            if request.GET.get('date'):
                date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
            else:    
                date = datetime.datetime.now() -  datetime.timedelta(days=1)

            context = {
                'vehicles' : AutographDailyIndicators.objects.filter(date=date.date()),
                'date' : date.strftime("%Y-%m-%d"),
            }
            return render(request, 'autographapp/autograph.html', context)    

        else:

            auth.logout(request)

            return render(request, 'cargoapp/menu/auth_role_error.html')    

    else:

        return redirect('login')        



def show_route(request, uid):

    if request.user.is_authenticated:

        users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()

        if request.user in users_in_group_logistsupervisor:

            context = {
                'route':  Route.objects.get(uid=uid)
            }

            return render(request, 'cargoapp/supervisor_route.html', context)

        else:    

            route = Route.objects.get(uid=uid)

            if route.organization:
                organizations = Organization.objects.filter(is_contragent=False).exclude(uid=route.organization.uid).order_by('title')
            else:  
                organizations = Organization.objects.filter(is_contragent=False).order_by('title')

            if route.contragent:
                contragents = Organization.objects.filter(is_contragent=True).exclude(uid=route.contragent.uid).order_by('title')
            else:  
                contragents = Organization.objects.filter(is_contragent=True).order_by('title')
                
            if route.driver:
                drivers = Driver.objects.all().exclude(uid=route.driver.uid).order_by('title')
            else:  
                drivers = Driver.objects.all().order_by('title')

            if route.logist:
                logists = LogistUser.objects.all().exclude(uid=route.logist.uid).order_by('username')
            else:  
                logists = LogistUser.objects.all().order_by('username')

            if route.vehicle:
                vehicles = Vehicle.objects.filter(logist=request.user).exclude(uid=route.vehicle.uid).order_by('car_number')
            else:  
                vehicles = Vehicle.objects.all().order_by('car_number')

            contracts = {}

            if route.organization and route.contragent:
                if route.contract:
                    contracts = Contracts.objects.filter(organization=route.organization, contragent=route.contragent).exclude(uid=route.contract.uid).order_by('date') 
                else:
                    contracts = Contracts.objects.filter(organization=route.organization, contragent=route.contragent).order_by('date') 
                

            context = {
                'route' : route,
                'drivers' : drivers,
                'logists' : logists,
                'vehicles' : vehicles,
                'cities'   : City.objects.all().order_by('title'),
                'organizations' : organizations,
                'contragents' : contragents,
                'contracts' : contracts,
            }

            return render(request, 'cargoapp/route.html', context)

    else:

        return redirect('login')            
    

def route_save(request, uid):

    if request.user.is_authenticated:

        if request.method == 'POST':

            route_form = RouteForm(request.POST, request.FILES)

            if route_form.is_valid():

                from_date = route_form.cleaned_data['inputFrom_date']
                to_date = route_form.cleaned_data['inputTo_date']
                a_point = route_form.cleaned_data['inputA_point']
                b_point = route_form.cleaned_data['inputB_point']
                route_length = route_form.cleaned_data['inputRoute_length']
                route_cost = route_form.cleaned_data['inputRoute_cost']
                expenses_1 = route_form.cleaned_data['inputExpenses_1']
                vehicle_uid = route_form.cleaned_data['inputVehicle']
                logist_uid = route_form.cleaned_data['inputLogist']
                driver_uid = route_form.cleaned_data['inputDriver']

                organization_uid = route_form.cleaned_data['inputOrganization']
                weight = route_form.cleaned_data['inputWeight']
                cargo_description = route_form.cleaned_data['inputDescription']
                request_number = route_form.cleaned_data['inputRequest_number']

                contragent_uid = route_form.cleaned_data['inputContragent']
                contract_uid = route_form.cleaned_data['inputContract']

                banner_all = route_form.cleaned_data['inputBanner_all']
                banner_side = route_form.cleaned_data['inputBanner_side']
                control_penalty = route_form.cleaned_data['inputControl_penalty']

                straight_boolean = route_form.cleaned_data['inputStraight_boolean']
                save_and_exit_boolean = route_form.cleaned_data['inputSaveAndExit_boolean']

                banner_a = route_form.cleaned_data['inputBanner_a']
                banner_b = route_form.cleaned_data['inputBanner_b']
                payment_type = route_form.cleaned_data['inputPayment_type']

                try:
                    request_img = request.FILES['inputRequest_img']
                except:
                    request_img = None
                    
                try:
                    loa_img = request.FILES['inputLoa_img']
                except:
                    loa_img = None    

                try:
                    current_route = Route.objects.get(uid=uid)
                except:
                    current_route = None

                if current_route:

                    if route_length:

                        current_route.route_length = Decimal(route_length.replace(',','.'))

                    else:
                        
                        gmaps = googlemaps.Client(key=config('GOOGLE_SECRET_KEY'))

                        try:
                            distance = gmaps.distance_matrix(origins=a_point, destinations=b_point, language='ru', mode='driving')['rows'][0]['elements'][0]
                        except:
                            distance = None
                            

                        try:
                            dist_length = json.dumps(distance.get('distance').get('text').split(' ')[0], ensure_ascii=False).replace('"', '')
                            dist_length = re.sub(r"\s+", "", dist_length, flags=re.UNICODE)
                        except:
                            messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!')
                            dist_length = 0

                        current_route.route_length = Decimal(dist_length)

                    current_route.from_date = from_date
                    current_route.to_date = to_date
                    current_route.a_point = a_point
                    current_route.b_point = b_point
                    current_route.cargo_description = cargo_description
                    current_route.request_number = request_number
                    
                    current_route.route_cost = Decimal(route_cost.replace(',','.')) if route_cost else Decimal(0).quantize(Decimal("1.00"))
                    current_route.expenses_1 = Decimal(expenses_1.replace(',','.')) if expenses_1 else Decimal(0).quantize(Decimal("1.00"))
                    current_route.weight = Decimal(weight.replace(',','.')) if weight else Decimal(0).quantize(Decimal("1.00"))

                    if request_img:
                        current_route.request_img = request_img

                    if loa_img:
                        current_route.loa_img = loa_img

                    current_route.banner_all = banner_all

                    current_route.banner_a = banner_a
                    current_route.banner_b = banner_b
                    current_route.payment_type = payment_type

                    current_route.banner_side = banner_side

                    current_route.control_penalty = control_penalty
                    
                    current_route.straight_boolean = straight_boolean

                    if vehicle_uid:
                        try:
                            current_vehicle = Vehicle.objects.get(uid=vehicle_uid)
                            current_route.vehicle = current_vehicle
                        except:
                            current_route.vehicle = None
                            messages.info(request, '???????????????????? ???????????????????? ???? ???????????????????? ?? ???????? ????????????!')           

                    if logist_uid:
                        try:
                            current_logist = LogistUser.objects.get(uid=logist_uid)
                            current_route.logist = current_logist
                        except:
                            current_route.logist = None
                            messages.info(request, '???????????????????? ?????????????? ???? ???????????????????? ?? ???????? ????????????!')           

                    if driver_uid:
                        try:
                            current_driver = Driver.objects.get(uid=driver_uid)
                            current_route.driver = current_driver
                        except:
                            current_route.logist = None
                            messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!')
                    else:
                        current_route.driver = None         

                    if organization_uid:
                        try:
                            current_organization = Organization.objects.get(uid=organization_uid)
                            current_route.organization = current_organization
                        except:
                            current_route.organization = None
                            messages.info(request, '?????????????????? ?????????????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                    else:
                        current_route.organization = None

                    if contragent_uid:
                        try:
                            current_contragent = Organization.objects.get(uid=contragent_uid)
                            current_route.contragent = current_contragent
                        except:
                            current_route.contragent = None
                            messages.info(request, '???????????????????? ?????????????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                    else:
                        current_route.contragent = None

                    if contract_uid:
                        try:
                            current_contract = Contracts.objects.get(uid=contract_uid)
                            current_route.contract = current_contract
                        except:
                            current_route.contract = None
                            messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                    else:
                        current_route.contract = None      
                    current_route.save()
                    if save_and_exit_boolean:
                        return redirect('show_index_page')
                    else:    
                        return redirect('show_route', uid=current_route.uid)

            else:

                messages.info(request, '?? ?????????? ?????????????? ???? ???????????????????? ????????????!')
                current_path = request.META['HTTP_REFERER']
                return redirect(current_path)

    else:

        return redirect('login')            


def route_add(request):

    if request.user.is_authenticated:

        if request.method == 'POST':

            route_form = RouteForm(request.POST, request.FILES)

            if route_form.is_valid():

                from_date = route_form.cleaned_data['inputFrom_date']
                to_date = route_form.cleaned_data['inputTo_date']
                a_point = route_form.cleaned_data['inputA_point']
                b_point = route_form.cleaned_data['inputB_point']
                route_length = route_form.cleaned_data['inputRoute_length']
                route_cost = route_form.cleaned_data['inputRoute_cost']
                expenses_1 = route_form.cleaned_data['inputExpenses_1']
                vehicle_uid = route_form.cleaned_data['inputVehicle']
                logist_uid = route_form.cleaned_data['inputLogist']
                driver_uid = route_form.cleaned_data['inputDriver']

                organization_uid = route_form.cleaned_data['inputOrganization']
                weight = route_form.cleaned_data['inputWeight']
                cargo_description = route_form.cleaned_data['inputDescription']
                request_number = route_form.cleaned_data['inputRequest_number']

                contragent_uid = route_form.cleaned_data['inputContragent']
                contract_uid = route_form.cleaned_data['inputContract']

                banner_all = route_form.cleaned_data['inputBanner_all']
                banner_side = route_form.cleaned_data['inputBanner_side']
                control_penalty = route_form.cleaned_data['inputControl_penalty']

                straight_boolean = route_form.cleaned_data['inputStraight_boolean']

                save_and_exit_boolean = route_form.cleaned_data['inputSaveAndExit_boolean']

                banner_a = route_form.cleaned_data['inputBanner_a']
                banner_b = route_form.cleaned_data['inputBanner_b']
                payment_type = route_form.cleaned_data['inputPayment_type']

                try:
                    request_img = request.FILES['inputRequest_img']
                except:
                    request_img = None
                    
                try:
                    loa_img = request.FILES['inputLoa_img']
                except:
                    loa_img = None 

                current_route = Route()

                current_route.from_date = from_date
                current_route.to_date = to_date
                current_route.a_point = a_point
                current_route.b_point = b_point
                current_route.cargo_description = cargo_description
                current_route.request_number = request_number


                if route_length:

                    current_route.route_length = Decimal(route_length.replace(',','.'))
                    

                else:

                    gmaps = googlemaps.Client(key=config('GOOGLE_SECRET_KEY'))

                    try:
                        distance = gmaps.distance_matrix(origins=a_point, destinations=b_point, language='ru', mode='driving')['rows'][0]['elements'][0]
                    except:
                        distance = None
                        

                    try:
                        dist_length = json.dumps(distance.get('distance').get('text').split(' ')[0], ensure_ascii=False).replace('"', '')
                        dist_length = re.sub(r"\s+", "", dist_length, flags=re.UNICODE)
                    except:
                        messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!')
                        dist_length = 0


                    current_route.route_length = Decimal(dist_length)

                if weight:
                    current_route.weight = Decimal(weight.replace(',','.'))
                else:
                    current_route.weight = Decimal(0)
       
                if route_cost:
                    current_route.route_cost = Decimal(route_cost.replace(',','.'))
                else:
                    current_route.route_cost = Decimal(0)

                if expenses_1:
                    current_route.expenses_1 = Decimal(expenses_1.replace(',','.'))
                else:
                    current_route.expenses_1 = Decimal(0)       
                
                if request_img:
                        current_route.request_img = request_img

                if loa_img:
                    current_route.loa_img = loa_img

                current_route.banner_all = banner_all

                current_route.banner_a = banner_a
                current_route.banner_b = banner_b
                current_route.payment_type = payment_type

                current_route.banner_side = banner_side

                current_route.control_penalty = control_penalty

                current_route.straight_boolean = straight_boolean

                if vehicle_uid:
                    try:
                        current_vehicle = Vehicle.objects.get(uid=vehicle_uid)
                        current_route.vehicle = current_vehicle
                    except:
                        current_route.vehicle = None
                        messages.info(request, '???????????????????? ???????????????????? ???? ???????????????????? ?? ???????? ????????????!')

                if logist_uid:
                    try:
                        current_logist = LogistUser.objects.get(uid=logist_uid)
                        current_route.logist = current_logist
                    except:
                        current_route.logist = None
                        messages.info(request, '???????????????????? ?????????????? ???? ???????????????????? ?? ???????? ????????????!')         

                if driver_uid:
                    try:
                        current_driver = Driver.objects.get(uid=driver_uid)
                        current_route.driver = current_driver
                    except:
                        current_route.logist = None
                        messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!') 
                else:
                        current_route.driver = None        
   
                if organization_uid:
                    try:
                        current_organization = Organization.objects.get(uid=organization_uid)
                        current_route.organization = current_organization
                    except:
                        current_route.organization = None
                        messages.info(request, '?????????????????? ?????????????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                else:
                    current_route.organization = None

                if contragent_uid:
                    try:
                        current_contragent = Organization.objects.get(uid=contragent_uid)
                        current_route.contragent = current_contragent
                    except:
                        current_route.contragent = None
                        messages.info(request, '???????????????????? ?????????????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                else:
                    current_route.contragent = None

                if contract_uid:
                    try:
                        current_contract = Contracts.objects.get(uid=contract_uid)
                        current_route.contract = current_contract
                    except:
                        current_route.contract = None
                        messages.info(request, '???????????????????? ???????????????? ???? ???????????????????? ?? ???????? ????????????!')                   
                else:
                    current_route.contract = None          

                current_route.save()

                if save_and_exit_boolean:
                    return redirect('show_index_page')
                else:    
                    return redirect('show_route', uid=current_route.uid)

            else:

                messages.info(request, '?? ?????????? ?????????????? ???? ???????????????????? ????????????!')
                current_path = request.META['HTTP_REFERER']
                return redirect(current_path)

    else:

        return redirect('login')
                

def show_new_route_form(request):

    if request.user.is_authenticated:

        context = {
            'drivers' : Driver.objects.all().order_by('title'),
            'logists' : LogistUser.objects.all().exclude(uid=request.user.uid).order_by('username'),
            'cities'   : City.objects.all().order_by('title'),
            'organizations' : Organization.objects.filter(is_contragent=False).order_by('title'),
            'contragents' : Organization.objects.filter(is_contragent=True).order_by('title'),
        }

        if request.GET.get('vehicle'):

            vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
            try:
                driver = Driver.objects.get(vehicle=vehicle)
            except:
                driver = None


            context.update({
                'actual_vehicle': vehicle,
                'actual_driver' : driver,
                'drivers' : Driver.objects.all().exclude(uid=driver.uid).order_by('title'),
                })


        return render(request, 'cargoapp/new_route.html', context) 

    else:

        return redirect('login')   


def delete_req_img(request, uid):
    try:
        route = Route.objects.get(uid=uid)
        route.request_img.delete()

        route.save()
    except:
        pass


    current_path = request.META['HTTP_REFERER']
    return redirect(current_path)

def delete_loa_img(request, uid):

    try:
        route = Route.objects.get(uid=uid)
        route.loa_img.delete()

        route.save()
    except:
        pass


    current_path = request.META['HTTP_REFERER']
    return redirect(current_path)


def routes_list(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()

        if request.user in users_in_group_logist:

            context = {

            }

            return render(request, 'cargoapp/routes_list/routes_list.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html') 

def holiday_requests(request):

    if request.user.is_authenticated:

        users_in_group_hr_dep = Group.objects.get(name="?????????? ????????????").user_set.all()

        if request.user in users_in_group_hr_dep:

            context = {

            }

            return render(request, 'cargoapp/hr_dep/holiday_request.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_daily_report(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor:

            context = {

            }

            return render(request, 'cargoapp/columnar/daily_report.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


#DRIVER

def driver_extra_repair(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/extra_repair.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_holiday_requests(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/holiday_requests.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_new_holiday_request(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/new_holiday_request.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_holiday_request(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/holiday_request.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_hr_change_date(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/hr_change_date.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_hr_without_changer(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/hr_without_changer.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_hr_drive_loaded(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/hr_drive_loaded.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_hr_accept(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/hr_accept.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_shift_change(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/shift_change/shift_change.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_shift_change_hand_over(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/shift_change/hand_over.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_shift_change_accept(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/shift_change/accept.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def driver_shift_change_accept_acc(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/shift_change/accept_acc.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def driver_shift_change_hand_over_acc(request):

    if request.user.is_authenticated:

        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()

        if request.user in users_in_group_driver:

            context = {

            }

            return render(request, 'cargoapp/driver/shift_change/hand_over_acc.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def documents_menu(request):

    if request.user.is_authenticated:

        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_hr_director = Group.objects.get(name="???????????????? ???? ??????????????????").user_set.all()

        if request.user in users_in_group_chief_column:
            return render(request, 'cargoapp/documents/chief_column_menu.html')
        if request.user in users_in_group_hr_director:
            return render(request, 'cargoapp/documents/hr_director_menu.html')
        else:
            return render(request, 'cargoapp/documents/menu.html')

def documents_agreement(request):

    if request.user.is_authenticated:
        return render(request, 'cargoapp/documents/agreement.html')

def documents_familiarize(request):

    if request.user.is_authenticated:
        return render(request, 'cargoapp/documents/familiarize.html')

def documents_all(request):

    if request.user.is_authenticated:
        return render(request, 'cargoapp/documents/all.html')

def documents_add(request):

     if request.user.is_authenticated:

        users_in_group_hr_director = Group.objects.get(name="???????????????? ???? ??????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_hr_director or request.user in users_in_group_chief_column:

            return render(request, 'cargoapp/documents/add.html')

def documents_report(request):

    if request.user.is_authenticated:

        users_in_group_hr_director = Group.objects.get(name="???????????????? ???? ??????????????????").user_set.all()

        if request.user in users_in_group_hr_director:

            return render(request, 'cargoapp/documents/report.html')


#COLUMNAR

def columnar_extra_repair(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/extra_repair.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_extra_repair_registration(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()


        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/extra_repair_registration.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')            

def columnar_holiday_requests(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/holiday_requests.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_single_holiday_requests(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/single_holiday_request.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_hr_change_date(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/hr_change_date.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def columnar_hr_without_changer(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/hr_without_changer.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')            

def columnar_hr_drive_loaded(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/hr_drive_loaded.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def columnar_shift_change_list(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_list.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')            

def columnar_maintenance_schedule_menu(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="?????????????? ????????????").user_set.all()
        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()

        if request.user in set(users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_logistsupervisor | users_in_group_logist):

            context = {

            }

            return render(request, 'cargoapp/columnar/maintenance_schedule/menu.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_maintenance_schedule_auto(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/maintenance_schedule/schedule_auto.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_maintenance_schedule_ref(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/maintenance_schedule/schedule_ref.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def columnar_vehicle_condition(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/vehicle/condition.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')
         

#LOGIST

def logist_extra_repair(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()

        if request.user in users_in_group_logist:

            context = {

            }

            return render(request, 'cargoapp/logist/extra_repair.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def logist_holiday_requests(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()

        if request.user in users_in_group_logist:

            context = {

            }

            return render(request, 'cargoapp/logist/holiday_requests.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def logist_holiday_request(request):

    if request.user.is_authenticated:

        users_in_group_logist = Group.objects.get(name="????????????").user_set.all()

        if request.user in users_in_group_logist:

            context = {

            }

            return render(request, 'cargoapp/logist/holiday_request.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

#GATE

def gate_shift_change_list(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_list.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def gate_shift_change_single(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_single.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_0.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_1(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_1.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_2(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_2.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_3(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_3.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_4(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_4.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_5(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_5.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_6(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_6.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_inspection_7(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_inspection_7.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def gate_shift_change_complete(request):

    if request.user.is_authenticated:

        users_in_group_vorotny = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_vorotny or request.user in users_in_group_vehicle_supervisor or request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/columnar/shift_change/shift_change_complete.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


# CHIEF COLUMN

def chief_column_daily_report(request):

    if request.user.is_authenticated:

        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()

        if request.user in users_in_group_chief_column:

            context = {

            }

            return render(request, 'cargoapp/chief_column/daily_report.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')



#health safety
def health_safety_journal_menu(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/menu.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def health_safety_journal_19_table(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook19/table.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def health_safety_journal_19_cover(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook19/cover.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')


def health_safety_journal_20_table(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook20/table.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def health_safety_journal_20_cover(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook20/cover.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')

def health_safety_journal_20_bage(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook20/bage.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')



def health_safety_journal_21_table(request):

    if request.user.is_authenticated:

        users_in_group_health_safety = Group.objects.get(name="???????????? ??????????").user_set.all()
        users_in_group_vehicle_supervisor = Group.objects.get(name="????????????????").user_set.all()
        users_in_group_chief_column = Group.objects.get(name="?????????????????? ????????????????").user_set.all()
        users_in_group_driver = Group.objects.get(name="????????????????").user_set.all()
    
        users_in_group = set(users_in_group_health_safety | users_in_group_vehicle_supervisor | users_in_group_chief_column | users_in_group_driver)

        if request.user in users_in_group:

            context = {

            }

            return render(request, 'cargoapp/health_safety/logbook21/table.html', context)

        else:

            return render(request, 'cargoapp/menu/auth_role_error.html')