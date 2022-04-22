from django.contrib import admin
from .models import LogistUser, Vehicle, Driver, Route, City
from .models import Organization, Contracts, Constant
from .models import MileageRevenueStandard, MileageThresholds, DailyIndicators

class LogistUserAdmin(admin.ModelAdmin):
	list_display = (
					'username',
					)
	# readonly_fields = ['uid',]
	# exclude = ['psw',]
admin.site.register(LogistUser, LogistUserAdmin)

class DriverAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					'experience'
					)
	readonly_fields = ('uid',)
	exclude = ['first_name', 'second_name', 'third_name']

	def experience(self, obj):

		return obj.get_experience()

admin.site.register(Driver, DriverAdmin)


class RouteAdmin(admin.ModelAdmin):

	list_display = (
					'id',
					'a_point',
					'b_point',
					'vehicle',
					)

	readonly_fields = ('uid','pay_check', 'straight')

	exclude = ['fuel_cost', 'pure_income', 'cost_of_km', 'cost_of_platon', 'day_count', ]

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
					'vin',
					'car_number',
					'nav_id',
					'logist',
					'driver'
					)

	list_filter = ('logist',)
	readonly_fields = ('uid', 'nav_id')

admin.site.register(Vehicle, VehicleAdmin)


class CityAdmin(admin.ModelAdmin):
	list_display = (
					'code',
					'title',
					'reduction',
					'lon',
					'lat',
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

	search_fields = ('title', 'full_title', 'inn', )

	readonly_fields = ('uid',)

admin.site.register(Organization, OrganizationAdmin)

class ContractsAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					'number',
					'date',
					'organization',
					'contragent'
					)

	list_filter = ('organization',)

	search_fields = ('title', 'number', 'date')

	readonly_fields = ('uid',)

admin.site.register(Contracts, ContractsAdmin)


class MileageRevenueStandardAdmin(admin.ModelAdmin):

	list_display = (
					'date',
					'vehicle',
					'mileage',
					'revenue',
					'net_income',
					)

admin.site.register(MileageRevenueStandard, MileageRevenueStandardAdmin)


class MileageThresholdsAdmin(admin.ModelAdmin):

	list_display = (
					'date',
					'mileage',
					'rate',
					)
	
admin.site.register(MileageThresholds, MileageThresholdsAdmin)

class DailyIndicatorsAdmin(admin.ModelAdmin):

	list_display = (
					'date',
					'mileage',
					'rate',
					'route'
					)

list_filter = ('route',)

admin.site.register(DailyIndicators,DailyIndicatorsAdmin)

class ConstantAdmin(admin.ModelAdmin):
	list_display = (
					'date',
					'title',
					'value',
					)
admin.site.register(Constant, ConstantAdmin)