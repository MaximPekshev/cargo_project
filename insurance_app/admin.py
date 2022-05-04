from django.contrib import admin
from .models import VehicleInsurance, ContragentInsurance, OwnerInsurance


class VehicleInsuranceAdmin(admin.ModelAdmin):
	list_display = (
					'vehicle',
					'type',
					'from_date',
					'to_date',
					'contragent',
					'owner',
					)

	search_fields = ('vehicle', )

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
