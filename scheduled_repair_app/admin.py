from django.contrib import admin

from .models import ServiceWork, ServiceWorkType, ServiceOrganization, ServiceWorkStatus



class ServiceWorkAdmin(admin.ModelAdmin):

    list_display = ('title',)
    readonly_fields = ('uid',)

admin.site.register(ServiceWork, ServiceWorkAdmin)


class ServiceWorkTypeAdmin(admin.ModelAdmin):

    list_display = ('title',)
    readonly_fields = ('uid',)

admin.site.register(ServiceWorkType, ServiceWorkTypeAdmin)

class ServiceOrganizationAdmin(admin.ModelAdmin):

    list_display = ('title',)
    readonly_fields = ('uid',)

admin.site.register(ServiceOrganization, ServiceOrganizationAdmin)


class ServiceWorkStatusAdmin(admin.ModelAdmin):

    list_display = ('title',)
    readonly_fields = ('uid',)

admin.site.register(ServiceWorkStatus, ServiceWorkStatusAdmin)
