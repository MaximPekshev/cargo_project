from django.contrib import admin
from .models import LogistUser, Vehicle, Driver, Route, City
from .models import Organization, Contracts

class LogistUserAdmin(admin.ModelAdmin):
	list_display = (
					'id',
					'username',
					'uid',
					)
	# readonly_fields = ['uid',]
	# exclude = ['psw',]
admin.site.register(LogistUser, LogistUserAdmin)

class DriverAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'title',
					)
	readonly_fields = ('uid',)
	exclude = ['first_name', 'second_name', 'third_name']

admin.site.register(Driver, DriverAdmin)


class RouteAdmin(admin.ModelAdmin):

	list_display = (
					'uid',
					'a_point',
					'b_point',
					'vehicle',
					)

	readonly_fields = ('uid',)

	exclude = ['fuel_cost', 'pay_check', 'pure_income', 'cost_of_km', 'cost_of_platon', 'day_count', ]

	# def formfield_for_foreignkey(self, db_field, request, **kwargs):
	# 	if db_field.name == "vehicle":
	# 		kwargs["queryset"] = Vehicle.objects.all().order_by('car_number')
	# 		return super(RouteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	# 	if db_field.name == "driver":
	# 		kwargs["queryset"] = Driver.objects.all().order_by('title')
	# 		return super(RouteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
			

admin.site.register(Route, RouteAdmin)

class VehicleAdmin(admin.ModelAdmin):
	list_display = (
					'uid',
					'vin',
					'car_number',
					)
	readonly_fields = ('uid',)

admin.site.register(Vehicle, VehicleAdmin)


class CityAdmin(admin.ModelAdmin):
	list_display = (
					'code',
					'title',
					'reduction',
					)
	readonly_fields = ('code',)

admin.site.register(City, CityAdmin)


class OrganizationAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					'inn',
					'kpp',
					'is_contragent',
					)

	list_filter = ('is_contragent',)

	search_fields = ('title', 'full_title', )

	readonly_fields = ('uid',)

	

admin.site.register(Organization, OrganizationAdmin)

class ContractsAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					'number',
					'date',
					)

	list_filter = ('organization',)

	search_fields = ('title', 'number', 'date')

	readonly_fields = ('uid',)


admin.site.register(Contracts, ContractsAdmin)