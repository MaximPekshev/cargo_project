from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='test'),
    path('test/<str:token>', views.finishedTest),
]
