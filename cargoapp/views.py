from calendar import month
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from .models import Vehicle
from .serializers import VehicleSerializer
from .models import Route
from .serializers import RouteSerializer
from .models import LogistUser
from .serializers import LogistUserSerializer
from .models import City
from .models import Organization
from .serializers import OrganizationSerializer
from .models import Contracts
from .serializers import ContractsSerializer
from django.contrib	import auth

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

from .forms import RouteForm
from django.contrib import messages
from decimal import Decimal

import googlemaps
import json
import re
from decouple import config

from django.db.models import Q

class ContractsList(generics.ListCreateAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()
        users_in_group_driver = Group.objects.get(name="Водитель").user_set.all()
        users_in_group_fuel_dep = Group.objects.get(name="Топливный отдел").user_set.all()
        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()

        if request.user in users_in_group_vehicle_supervisor:

            return render(request, 'cargoapp/menu/vehicle_sv_menu.html')
        
        elif request.user in users_in_group_logistsupervisor:

            return render(request, 'cargoapp/menu/supervisor_menu.html')

        elif request.user in users_in_group_driver:
             
            return render(request, 'cargoapp/menu/driver_menu.html')

        elif request.user in users_in_group_fuel_dep:
             
            return render(request, 'cargoapp/menu/fuel_dep_menu.html')    

        elif request.user in users_in_group_logist:

            return render(request, 'cargoapp/menu/logist_menu.html')

        else:

            auth.logout(request)

            return render(request, 'cargoapp/menu/auth_role_error.html')
    else:

        return redirect('login') 
        
def show_index_page(request):

    if request.user.is_authenticated:

        users_in_group_vehicle_supervisor = Group.objects.get(name="Колонный").user_set.all()
        users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()
        users_in_group_logist = Group.objects.get(name="Логист").user_set.all()

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

            logists  = LogistUser.objects.filter(supervisor=request.user)
            vehicle = None
            logist = None

            if request.GET.get('vehicle') and not request.GET.get('logist'):
                vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
                routes = Route.objects.filter(vehicle=vehicle).order_by('logist', '-from_date')
            elif not request.GET.get('vehicle') and request.GET.get('logist'):
                logist = LogistUser.objects.get(uid=request.GET.get('logist'))
                routes = Route.objects.filter(logist=logist).order_by('logist', '-from_date')
            elif request.GET.get('vehicle') and request.GET.get('logist'):
                vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
                logist = LogistUser.objects.get(uid=request.GET.get('logist'))
                routes = Route.objects.filter(logist=logist, vehicle=vehicle).order_by('logist', '-from_date')
            else:
                routes = Route.objects.filter(logist__in=logists).order_by('logist', '-from_date')
                vehicle = None

            if vehicle:
                vehicles = Vehicle.objects.filter(logist__in=logists).exclude(uid=vehicle.uid)
            else:
                vehicles = Vehicle.objects.filter(logist__in=logists)

            if logist:
                logists =  LogistUser.objects.filter(supervisor=request.user).exclude(uid=logist.uid)
                vehicles = Vehicle.objects.filter(logist=logist)
            else:
                logists = LogistUser.objects.filter(supervisor=request.user)   

            try:
                # total_routes_length = routes.aggregate(Sum('route_length'))['route_length__sum']
                total_cost_of_km = ((routes.aggregate(Sum('route_cost'))['route_cost__sum']/routes.aggregate(Sum('route_length'))['route_length__sum']).quantize(Decimal("1.00")))
            except:
                total_cost_of_km = Decimal(0)
                total_cost_of_km = total_cost_of_km.quantize(Decimal("1.00")) 

            context = {
                'user' : request.user,
                'routes' : routes,
                'vehicles' : vehicles,
                'logists' : logists,
                'checked_vehicle': vehicle,
                'checked_logist': logist,
                'total_expenses_1' : routes.aggregate(Sum('expenses_1'))['expenses_1__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_route_cost' : routes.aggregate(Sum('route_cost'))['route_cost__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_route_length' : routes.aggregate(Sum('route_length'))['route_length__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_days' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_fuel_cost' : routes.aggregate(Sum('fuel_cost'))['fuel_cost__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pay_check' : routes.aggregate(Sum('pay_check'))['pay_check__sum'].quantize(Decimal("1.00")) if routes else 0,
                'total_pure_income' : ((routes.aggregate(Sum('pure_income'))['pure_income__sum']-routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum']).quantize(Decimal("1.00"))) if routes else 0,
                'total_cost_of_km' : total_cost_of_km,
                'total_cost_of_platon' : routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum'].quantize(Decimal("1.00")) if routes else 0 if routes else 0,
                'total_day_count' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")) if routes else 0,
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

            try:
                plan_total_cost_of_km = Decimal(revenueStandard/mileageStandard).quantize(Decimal("1.00"))
            except:        
                plan_total_cost_of_km = Decimal(0).quantize(Decimal("1.00"))

            #фактические данные
            total_route_length = routes.aggregate(Sum('route_length'))['route_length__sum'].quantize(Decimal("1.00")) if routes else 0
            total_route_cost = routes.aggregate(Sum('route_cost'))['route_cost__sum'].quantize(Decimal("1.00")) if routes else 0
            total_pure_income = routes.aggregate(Sum('straight'))['straight__sum'].quantize(Decimal("1.00"))if routes else 0

            #расчет плановых значений
            plan_total_route_length = Decimal(mileageStandard).quantize(Decimal("1.00"))
            plan_total_route_cost = Decimal(revenueStandard).quantize(Decimal("1.00"))
            plan_total_pure_income = Decimal(net_incomeStandart).quantize(Decimal("1.00"))

            #расчет остатков до плана
            route_length_diff = plan_total_route_length - total_route_length
            route_cost_diff = plan_total_route_cost - total_route_cost
            cost_of_km_diff = plan_total_cost_of_km - total_cost_of_km
            pure_income_diff = plan_total_pure_income - total_pure_income

            #расчет процента выполнения
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

        else:

            auth.logout(request)

            return render(request, 'cargoapp/menu/auth_role_error.html')    

    else:

        return redirect('login')        



def show_route(request, uid):

    if request.user.is_authenticated:

        users_in_group_logistsupervisor = Group.objects.get(name="Старший логист").user_set.all()

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
                            messages.info(request, 'Выбранного Маршрута не существует в базе данных!')
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

                    current_route.banner_side = banner_side

                    current_route.control_penalty = control_penalty
                    
                    current_route.straight_boolean = straight_boolean

                    if vehicle_uid:
                        try:
                            current_vehicle = Vehicle.objects.get(uid=vehicle_uid)
                            current_route.vehicle = current_vehicle
                        except:
                            current_route.vehicle = None
                            messages.info(request, 'Выбранного Автомобиля не существует в базе данных!')           

                    if logist_uid:
                        try:
                            current_logist = LogistUser.objects.get(uid=logist_uid)
                            current_route.logist = current_logist
                        except:
                            current_route.logist = None
                            messages.info(request, 'Выбранного Логиста не существует в базе данных!')           

                    if driver_uid:
                        try:
                            current_driver = Driver.objects.get(uid=driver_uid)
                            current_route.driver = current_driver
                        except:
                            current_route.logist = None
                            messages.info(driver, 'Выбранного Водителя не существует в базе данных!')
                    else:
                        current_route.driver = None         

                    if organization_uid:
                        try:
                            current_organization = Organization.objects.get(uid=organization_uid)
                            current_route.organization = current_organization
                        except:
                            current_route.organization = None
                            messages.info(request, 'Выбранной Организации не существует в базе данных!')                   
                    else:
                        current_route.organization = None

                    if contragent_uid:
                        try:
                            current_contragent = Organization.objects.get(uid=contragent_uid)
                            current_route.contragent = current_contragent
                        except:
                            current_route.contragent = None
                            messages.info(request, 'Выбранного Контрагента не существует в базе данных!')                   
                    else:
                        current_route.contragent = None

                    if contract_uid:
                        try:
                            current_contract = Contracts.objects.get(uid=contract_uid)
                            current_route.contract = current_contract
                        except:
                            current_route.contract = None
                            messages.info(request, 'Выбранного Договора не существует в базе данных!')                   
                    else:
                        current_route.contract = None      
           
                    current_route.save()

                    current_path = request.META['HTTP_REFERER']
                    return redirect(current_path)

            else:

                messages.info(request, 'В форму введены не корректные данные!')
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

                banner_all = route_form.cleaned_data['inputBanner_all']
                banner_side = route_form.cleaned_data['inputBanner_side']
                control_penalty = route_form.cleaned_data['inputControl_penalty']

                straight_boolean = route_form.cleaned_data['inputStraight_boolean']


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
                        messages.info(request, 'Выбранного Маршрута не существует в базе данных!')
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

                current_route.banner_side = banner_side

                current_route.control_penalty = control_penalty

                current_route.straight_boolean = straight_boolean

                if vehicle_uid:
                    try:
                        current_vehicle = Vehicle.objects.get(uid=vehicle_uid)
                        current_route.vehicle = current_vehicle
                    except:
                        current_route.vehicle = None
                        messages.info(request, 'Выбранного Автомобиля не существует в базе данных!')

                if logist_uid:
                    try:
                        current_logist = LogistUser.objects.get(uid=logist_uid)
                        current_route.logist = current_logist
                    except:
                        current_route.logist = None
                        messages.info(request, 'Выбранного Логиста не существует в базе данных!')         

                if driver_uid:
                    try:
                        current_driver = Driver.objects.get(uid=driver_uid)
                        current_route.driver = current_driver
                    except:
                        current_route.logist = None
                        messages.info(request, 'Выбранного Водителя не существует в базе данных!') 
                else:
                        current_route.driver = None        
   
                if organization_uid:
                    try:
                        current_organization = Organization.objects.get(uid=organization_uid)
                        current_route.organization = current_organization
                    except:
                        current_route.organization = None
                        messages.info(request, 'Выбранной Организации не существует в базе данных!')                   
                else:
                    current_route.organization = None

                if contragent_uid:
                    try:
                        current_contragent = Organization.objects.get(uid=contragent_uid)
                        current_route.contragent = current_contragent
                    except:
                        current_route.contragent = None
                        messages.info(request, 'Выбранного Контрагента не существует в базе данных!')                   
                else:
                    current_route.contragent = None         

                current_route.save()

                return redirect('show_route', uid=current_route.uid)

            else:

                messages.info(driver, 'В форму введены не корректные данные!')
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