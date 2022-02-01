from django.contrib import admin

from .models import AutographDailyIndicators


class AutographDailyIndicatorsAdmin(admin.ModelAdmin):

	list_display = (
					'date',
					'vehicle',
					'driver'
					)
	readonly_fields = ('date',)
	list_filter = ('vehicle',)

admin.site.register(AutographDailyIndicators, AutographDailyIndicatorsAdmin)
