from .models import Driver, Vehicle, Route
from django.contrib.auth.models import User
from rest_framework import serializers


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'uid', 'first_name', 'second_name', 'third_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'uid', 'vin', 'car_number', 'logist']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'id',
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
            'logist',
        ]        