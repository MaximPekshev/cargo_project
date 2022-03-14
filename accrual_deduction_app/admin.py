from django.contrib import admin
from .models import AccrualDeduction, ReasonOfDeduction


class AccrualDeductionAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'vehicle', 
        'logist',
    )
    readonly_fields = (
        'uid',
    )
admin.site.register(AccrualDeduction, AccrualDeductionAdmin)


class ReasonOfDeductionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
admin.site.register(ReasonOfDeduction, ReasonOfDeductionAdmin)