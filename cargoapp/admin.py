from django.contrib import admin
from .models import Vehicle, Driver, Route

class VehicleAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'vin',
					'car_number',
					)

admin.site.register(Vehicle, VehicleAdmin)


class DriverAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'first_name',
					'second_name',
					'third_name',
					)

admin.site.register(Driver, DriverAdmin)


class RouteAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'a_point',
					'b_point',
					'vehicle',
					)

admin.site.register(Route, RouteAdmin)