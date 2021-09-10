from django.urls import path
from .views import show_index_page, show_route, route_save, route_add, show_new_route_form

urlpatterns = [
	path('', 	show_index_page , name='show_index_page'),
	path('routes/new-route-form/', 	show_new_route_form , name='show_new_route_form'),
	path('routes/add/', 	route_add , name='route_add'),
	path('routes/<str:uid>/', 	show_route , name='show_route'),
	path('routes/save/<str:uid>/', 	route_save , name='route_save'),
]
