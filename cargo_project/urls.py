
from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', include('cargoapp.urls')),
    path('auth/', include('authapp.urls')),
    path('autograph/', include('autographapp.urls')),
    path('accrural-deduction/', include('accrual_deduction_app.urls')),
    path('api/v1/', include('api_app.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('mobi-fuel/', include('mobiFuel.urls')),
    path('mobi-group/', include('mobiGroup.urls')),
    path('requests/', include('request_app.urls')),
    path('insurance/', include('insurance_app.urls')),
    path('line-release/', include('line_release_app.urls')),
    path('scheduled-repair/', include('scheduled_repair_app.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()