from django.contrib import admin
from .models import VehicleInsurance, ContragentInsurance, OwnerInsurance
from .models import TrailerInsurance

class VehicleInsuranceAdmin(admin.ModelAdmin):
	list_display = (
					'vehicle',
					'type',
					'from_date',
					'to_date',
					'contragent',
					'owner',
					)

	search_fields = ('vehicle__uid', 'vehicle__vin', 'vehicle__car_number')

admin.site.register(VehicleInsurance, VehicleInsuranceAdmin)


class ContragentInsuranceAdmin(admin.ModelAdmin):
	list_display = (
                    'id',
					'title',
					)

	search_fields = ('title', )

admin.site.register(ContragentInsurance, ContragentInsuranceAdmin)


class OwnerInsuranceAdmin(admin.ModelAdmin):
	list_display = (
                    'id',
					'title',
					)

	search_fields = ('title', )

admin.site.register(OwnerInsurance, OwnerInsuranceAdmin)

class TrailerInsuranceAdmin(admin.ModelAdmin):
	list_display = (
					'trailer',
					'type',
					'from_date',
					'to_date',
					'contragent',
					'owner',
					)

	search_fields = ('trailer__uid', 'trailer__vin', 'trailer__number')

admin.site.register(TrailerInsurance, TrailerInsuranceAdmin)