from django.shortcuts import render
from rest_framework import viewsets
from .models import Driver
from .serializers import DriverSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Vehicle
from .serializers import VehicleSerializer
from .models import Route
from .serializers import RouteSerializer

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

class DriverDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Driver.objects.all()
	serializer_class = DriverSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # def get_object(self, pk):
    #     try:
    #         return Driver.objects.get(pk=pk)
    #     except Driver.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
	   # 	driver = self.get_object(pk)
	   # 	serializer = DriverSerializer(driver)
	   # 	return Response(serializer.data)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RouteList(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RouteDetail(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]