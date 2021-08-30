from django.contrib import admin
from .models import LogistUser, Vehicle, Driver, Route

class LogistUserAdmin(admin.ModelAdmin):
	list_display = (
					'id',
					'username',
					'uid',
					)
	readonly_fields = ['uid',]
admin.site.register(LogistUser, LogistUserAdmin)

class DriverAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'title',
					'first_name',
					'second_name',
					'third_name',
					)
	readonly_fields = ('uid',)

admin.site.register(Driver, DriverAdmin)


class RouteAdmin(admin.ModelAdmin):

	list_display = (
					'uid',
					'a_point',
					'b_point',
					'vehicle',
					)

	readonly_fields = ('uid',) 

admin.site.register(Route, RouteAdmin)

class VehicleAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'vin',
					'car_number',
					)
	readonly_fields = ('uid',)

admin.site.register(Vehicle, VehicleAdmin)