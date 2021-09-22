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


class DriverList(generics.ListCreateAPIView):
	queryset = Driver.objects.all()
	serializer_class = DriverSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LogistUserList(generics.ListCreateAPIView):
    queryset = LogistUser.objects.all()
    serializer_class = LogistUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LogistUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LogistUser.objects.all()
    serializer_class = LogistUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uid'

class RouteList(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    
def show_index_page(request):

    if request.user.is_authenticated:

        if request.GET.get('vehicle'):
            vehicle = Vehicle.objects.get(uid=request.GET.get('vehicle'))
            routes = Route.objects.filter(logist=request.user, vehicle=vehicle)
        else:
            routes = Route.objects.filter(logist=request.user)
            vehicle = None


        context = {
             'user' : request.user,
             'routes' : routes,
             'vehicles' : Vehicle.objects.filter(logist=request.user),
             'actual_vehicle': vehicle,
             'total_expenses_1' : routes.aggregate(Sum('expenses_1'))['expenses_1__sum'].quantize(Decimal("1.00")),
             'total_route_cost' : routes.aggregate(Sum('route_cost'))['route_cost__sum'].quantize(Decimal("1.00")),
             'total_route_length' : routes.aggregate(Sum('route_length'))['route_length__sum'].quantize(Decimal("1.00")),
             'total_days' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")),
             'total_fuel_cost' : routes.aggregate(Sum('fuel_cost'))['fuel_cost__sum'].quantize(Decimal("1.00")),
             'total_pay_check' : routes.aggregate(Sum('pay_check'))['pay_check__sum'].quantize(Decimal("1.00")),
             'total_pure_income' : (routes.aggregate(Sum('pure_income'))['pure_income__sum']-routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum']).quantize(Decimal("1.00")),
             'total_cost_of_km' : (routes.aggregate(Sum('route_cost'))['route_cost__sum']/routes.aggregate(Sum('route_length'))['route_length__sum']).quantize(Decimal("1.00")),
             'total_cost_of_platon' : routes.aggregate(Sum('cost_of_platon'))['cost_of_platon__sum'].quantize(Decimal("1.00")),
             'total_day_count' : routes.aggregate(Sum('day_count'))['day_count__sum'].quantize(Decimal("1.00")),
        }

        return render(request, 'cargoapp/index_page.html', context)

    else:

        return redirect('login')        


def show_route(request, uid):

    if request.user.is_authenticated:

        route = Route.objects.get(uid=uid)

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
            

        context = {
            'route' : route,
            'drivers' : drivers,
            'logists' : logists,
            'vehicles' : vehicles,
            'cities'   : City.objects.all().order_by('title'),
        }

        return render(request, 'cargoapp/route.html', context)

    else:

        return redirect('login')            
    

def route_save(request, uid):

    if request.user.is_authenticated:

        if request.method == 'POST':

            route_form = RouteForm(request.POST)

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

                try:
                    current_route = Route.objects.get(uid=uid)
                except:
                    current_route = None

                if current_route:

                    if route_length:

                        current_route.route_length = Decimal(route_length.replace(',','.'))

                    else:
                        
                        gmaps = googlemaps.Client(key='AIzaSyAUMjzkYbazeZE43K_-OUAWSnhE3_OA3TY')

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
                    
                    current_route.route_cost = Decimal(route_cost.replace(',','.'))
                    current_route.expenses_1 = Decimal(expenses_1.replace(',','.'))

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

                    current_route.save()

                    current_path = request.META['HTTP_REFERER']
                    return redirect(current_path)

            else:

                messages.info(driver, 'В форму введены не корректные данные!')
                current_path = request.META['HTTP_REFERER']
                return redirect(current_path)

    else:

        return redirect('login')            


def route_add(request):

    if request.user.is_authenticated:

        if request.method == 'POST':

            route_form = RouteForm(request.POST)

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

                current_route = Route()

                current_route.from_date = from_date
                current_route.to_date = to_date
                current_route.a_point = a_point
                current_route.b_point = b_point

                if route_length:

                    current_route.route_length = Decimal(route_length.replace(',','.'))
                    

                else:

                    gmaps = googlemaps.Client(key='AIzaSyAUMjzkYbazeZE43K_-OUAWSnhE3_OA3TY')

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

                if route_cost:
                    current_route.route_cost = Decimal(route_cost.replace(',','.'))
                else:
                    current_route.route_cost = Decimal(0)

                if expenses_1:
                    current_route.expenses_1 = Decimal(expenses_1.replace(',','.'))
                else:
                    current_route.expenses_1 = Decimal(0)       
                

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