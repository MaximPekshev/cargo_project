from django.urls import path
from .views import show_index_page, show_route, route_save, route_add, show_new_route_form
from .views import delete_req_img, delete_loa_img, show_menu_page
from .views import routes_list, holiday_requests, columnar_daily_report
#driver
from .views import driver_extra_repair
#columnar
from .views import columnar_extra_repair
#logist
from .views import logist_extra_repair

urlpatterns = [
	path('', 	show_menu_page , name='show_menu_page'),
	path('main/', 	show_index_page , name='show_index_page'),
	path('routes/delete-req-img/<str:uid>/', 	delete_req_img , name='delete_req_img'),
	path('routes/delete-loa-img/<str:uid>/', 	delete_loa_img , name='delete_loa_img'),
	path('routes/new-route-form/', 	show_new_route_form , name='show_new_route_form'),
	path('routes/add/', 	route_add , name='route_add'),
	path('routes/<str:uid>/', 	show_route , name='show_route'),
	path('routes/save/<str:uid>/', 	route_save , name='route_save'),
	path('routes-list/', 	routes_list , name='routes_list'),
	path('hr/holiday-requests/', 	holiday_requests , name='holiday_requests'),
	path('columnar/daily-report/', 	columnar_daily_report , name='columnar_daily_report'),

	path('driver/extra-repair/', 	driver_extra_repair , name='driver_extra_repair'),
	path('columnar/extra-repair/', 	columnar_extra_repair , name='columnar_extra_repair'),
	path('logist/extra-repair/', 	logist_extra_repair , name='logist_extra_repair'),

]
