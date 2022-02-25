from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='mobi_group_test'),
    path('test/<str:token>', views.finishedTest, name='mobi_group_test_result'),
]
