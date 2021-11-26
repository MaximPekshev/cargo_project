from django.urls import path
from django.urls import include
from rest_framework import routers
from cargoapp.views import DriverList, DriverDetail
from cargoapp.views import LogistUserList, LogistUserDetail
from cargoapp.views import VehicleList, VehicleDetail
from cargoapp.views import RouteList, RouteDetail
from cargoapp.views import OrganizationList, OrganizationDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('drivers/', DriverList.as_view()),
	path('drivers/<str:uid>/', DriverDetail.as_view()),
	path('users/', LogistUserList.as_view()),
    path('users/<str:uid>/', LogistUserDetail.as_view()),
    path('vehicles/', VehicleList.as_view()),
    path('vehicles/<str:uid>/', VehicleDetail.as_view()),
    path('routes/', RouteList.as_view()),
    path('routes/<str:uid>/', RouteDetail.as_view()),
    path('organizations/', OrganizationList.as_view()),
    path('organizations/<str:uid>/', OrganizationDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)