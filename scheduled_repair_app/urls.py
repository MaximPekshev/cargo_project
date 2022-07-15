from django.urls import path
from .views import show_scheduled_repair_list, scheduled_repair_new, scheduled_repair_add, scheduled_repair_object
from .views import scheduled_repair_save, show_scheduled_plan_fact_vehicle_list


urlpatterns = [

    path('plan-fact/vehicle', 	show_scheduled_plan_fact_vehicle_list , name='show_scheduled_plan_fact_vehicle_list'),
    path('list/', 	show_scheduled_repair_list , name='show_scheduled_repair_list'),
    path('new/', 	scheduled_repair_new, name='scheduled_repair_new'),
    path('add/', 	scheduled_repair_add, name='scheduled_repair_add'),
    path('save/<str:pk>', 	scheduled_repair_save, name='scheduled_repair_save'),
    path('<str:pk>', 	scheduled_repair_object, name='scheduled_repair_object'),
    
]