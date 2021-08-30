from .models import Driver, Vehicle, Route, LogistUser
from rest_framework import serializers


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('uid', 'title', 'first_name', 'second_name', 'third_name')


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['uid', 'vin', 'car_number', 'driver', 'logist']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'uid',
            'from_date',
            'to_date',
            'a_point',
            'b_point',
            'route_length',
            'route_cost',
            'expenses_1',
            'expenses_2',
            'expenses_3',
            'vehicle',
            'driver',
        ]

class LogistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogistUser
        fields = ('uid', 'username', 'is_active', 'psw', 'is_staff')
