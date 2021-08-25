from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import DriverList, DriverDetail
from .views import UserList, UserDetail
from .views import VehicleList, VehicleDetail
from .views import RouteList, RouteDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('drivers/', DriverList.as_view()),
	path('drivers/<int:pk>/', DriverDetail.as_view()),
	path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('vehicles/', VehicleList.as_view()),
    path('vehicles/<int:pk>/', VehicleDetail.as_view()),
    path('routes/', RouteList.as_view()),
    path('routes/<int:pk>/', RouteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)