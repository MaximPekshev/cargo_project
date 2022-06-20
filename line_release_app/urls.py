from django.urls import path
from .views import show_line_release_list

urlpatterns = [
    path('', 	show_line_release_list , name='show_line_release_list'),
]