from django.shortcuts import render
from rest_framework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from .models import Vehicle
from .serializers import VehicleSerializer
from .models import Route
from .serializers import RouteSerializer
from .models import LogistUser
from .serializers import LogistUserSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions



class DriverList(generics.ListCreateAPIView):
	queryset = Driver.objects.all()
	serializer_class = DriverSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	 # def get(self, request, format=None):
	 # 	drivers = Driver.objects.all()
	 # 	serializer = DriverSerializer(drivers, many=True)
	 # 	return Response(serializer.data)

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
    
    # def get_object(self, pk):
    #     try:
    #         return Driver.objects.get(pk=pk)
    #     except Driver.DoesNotExist:
    #         raise Http404

    # def get(self, request, uid, format=None):
    #     driver = self.get_object(pk)
    #     serializer = DriverSerializer(driver)
    #     return Response(serializer.data)
