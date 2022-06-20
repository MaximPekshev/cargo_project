from django.contrib import admin
from .models import LineRelease


class LineReleaseAdmin(admin.ModelAdmin):
    
    list_display = (
        'uid',
        'begin_date',
        'end_date',
        'vehicle',
        'trailer', 
        'driver',
    )

    readonly_fields = ('end_date',)

admin.site.register(LineRelease, LineReleaseAdmin)