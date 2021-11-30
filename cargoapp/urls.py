from django.urls import path
from .views import show_index_page, show_route, route_save, route_add, show_new_route_form
from .views import delete_req_img, delete_loa_img

urlpatterns = [
	path('', 	show_index_page , name='show_index_page'),
	path('routes/delete-req-img/<str:uid>/', 	delete_req_img , name='delete_req_img'),
	path('routes/delete-loa-img/<str:uid>/', 	delete_loa_img , name='delete_loa_img'),
	path('routes/new-route-form/', 	show_new_route_form , name='show_new_route_form'),
	path('routes/add/', 	route_add , name='route_add'),
	path('routes/<str:uid>/', 	show_route , name='show_route'),
	path('routes/save/<str:uid>/', 	route_save , name='route_save'),
]
