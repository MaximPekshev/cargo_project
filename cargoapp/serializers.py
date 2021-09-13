from .models import Driver, Vehicle, Route, LogistUser
from rest_framework import serializers


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('uid', 'title')

class LogistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogistUser
        fields = ('uid', 'username', 'is_active', 'psw', 'is_staff')        


class VehicleSerializer(serializers.ModelSerializer):
    driver_uid = serializers.CharField(source='driver.uid', required=False)
    logist_uid = serializers.CharField(source='logist.uid', required=False)
    class Meta:
        model = Vehicle
        fields = ('uid', 'vin', 'car_number', 'driver_uid', 'logist_uid')


    def create(self, validated_data):
        driver_uid = validated_data.pop('driver')
        logist_uid = validated_data.pop('logist')
        instance = Vehicle.objects.create(**validated_data)
        try:
            driver = Driver.objects.get(uid=driver_uid.get('uid'))
        except:
            driver = None
        try:
            logist = LogistUser.objects.get(uid=logist_uid.get('uid'))
        except:
            logist = None    
        instance.driver = driver
        instance.logist = logist  
        return instance

    def update(self, instance, validated_data):
        driver_uid = validated_data.pop('driver')
        logist_uid = validated_data.pop('logist')
        instance = super().update(instance, validated_data)
        try:
            driver = Driver.objects.get(uid=driver_uid.get('uid'))
        except:
            driver = None
        try:
            logist = LogistUser.objects.get(uid=logist_uid.get('uid'))
        except:
            logist = None    
        instance.driver = driver
        instance.logist = logist  
        return instance 

class RouteSerializer(serializers.ModelSerializer):

    vehicle = VehicleSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    logist = LogistUserSerializer(read_only=True)

    class Meta:
        model = Route
        fields = (
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
            'logist'
        )


