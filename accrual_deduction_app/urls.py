from django.urls import path
from .views import accrual_deduction_list
from .views import new_accrual_deduction
from .views import add_accrual_deduction
from .views import show_accrual_deduction
from .views import save_accrual_deduction

urlpatterns = [
	path('', 	accrual_deduction_list , name='accrual_deduction_list'),
	path('add/', 	add_accrual_deduction , name='add_accrual_deduction'),
	path('new/', 	new_accrual_deduction , name='new_accrual_deduction'),
	path('save/<str:uid>/', 	save_accrual_deduction , name='save_accrual_deduction'),
	path('<str:uid>/', 	show_accrual_deduction , name='show_accrual_deduction'),
]
