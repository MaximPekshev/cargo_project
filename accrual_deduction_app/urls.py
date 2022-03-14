from django.urls import path
from .views import show_accrual_deduction
from .views import new_accrual_deduction

urlpatterns = [
	path('', 	show_accrual_deduction , name='show_accrual_deduction'),
	path('new-accrural/', 	new_accrual_deduction , name='new_accrual_deduction'),
]
