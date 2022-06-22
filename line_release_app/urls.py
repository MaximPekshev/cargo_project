from django.urls import path
from .views import show_line_release_list, line_release_add, line_release_new

urlpatterns = [
    path('', 	show_line_release_list , name='show_line_release_list'),
    path('new/', 	line_release_new , name='line_release_new'),
    path('add/', 	line_release_add , name='line_release_add'),
]