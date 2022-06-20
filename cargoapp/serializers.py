from .models import Driver, Vehicle, Route
from .models import LogistUser, Organization, Contracts
from .models import City
from rest_framework import serializers

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('code', 'title', 'reduction', 'lon', 'lat', 'region_code', )

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'uid',
            'title',
            'full_title',
            'inn',
            'kpp',
            'ogrn',
            'address',
            'nds',
            'bank_account',
            'bank_bik',
            'bank_corr',
            'bank_title',
            'is_contragent',
            )

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('uid', 'title', 'employment_date',)

class LogistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogistUser
        fields = ('uid', 'username', 'is_active', 'psw', 'is_staff')        


class VehicleSerializer(serializers.ModelSerializer):
    driver_uid = serializers.CharField(source='driver.uid', required=False)
    logist_uid = serializers.CharField(source='logist.uid', required=False)
    class Meta:
        model = Vehicle
        fields = ('uid', 'vin', 'car_number', 'employment_date', 'driver_uid', 'logist_uid', 'nav_id',)


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
        instance.save()
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
        instance.save()
        return instance 

class RouteSerializer(serializers.ModelSerializer):

    vehicle = VehicleSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    logist = LogistUserSerializer(read_only=True)
    client = OrganizationSerializer(read_only=True)

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
            'logist',
            'client',
        )


class ContractsSerializer(serializers.ModelSerializer):

    organization_uid = serializers.CharField(source='organization.uid', required=False)
    contragent_uid = serializers.CharField(source='contragent.uid', required=False)

    class Meta:

        model = Contracts
        fields = (
            'uid',
            'title',
            'number',
            'date',
            'organization_uid',
            'contragent_uid',
        )

    def create(self, validated_data):
        organization_uid = validated_data.pop('organization')
        contragent_uid = validated_data.pop('contragent')
        instance = Contracts.objects.create(**validated_data)
        try:
            organization = Organization.objects.get(uid=organization_uid.get('uid'))
        except:
            organization = None
        try:
            contragent = Organization.objects.get(uid=contragent_uid.get('uid'))
        except:
            contragent = None    
        instance.organization = organization
        instance.contragent = contragent  
        instance.save()
        return instance

    def update(self, instance, validated_data):
        organization_uid = validated_data.pop('organization')
        contragent_uid = validated_data.pop('contragent')
        instance = super().update(instance, validated_data)
        try:
            organization = Organization.objects.get(uid=organization_uid.get('uid'))
        except:
            organization = None
        try:
            contragent = Organization.objects.get(uid=contragent_uid.get('uid'))
        except:
            contragent = None    
        instance.organization = organization
        instance.contragent = contragent
        instance.save()
        return instance     