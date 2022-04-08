from django.urls import path
from .views import show_index_page, show_route, route_save, route_add, show_new_route_form
from .views import delete_req_img, delete_loa_img, show_menu_page
from .views import routes_list, holiday_requests, columnar_daily_report
#driver
from .views import driver_extra_repair
from .views import driver_holiday_requests
from .views import driver_new_holiday_request
from .views import driver_holiday_request
from .views import driver_hr_change_date
from .views import driver_hr_without_changer
from .views import driver_hr_drive_loaded
from .views import driver_hr_accept
from .views import driver_shift_change
from .views import driver_shift_change_hand_over
from .views import driver_shift_change_accept
from .views import driver_shift_change_accept_acc
from .views import driver_shift_change_hand_over_acc

#columnar
from .views import columnar_extra_repair
from .views import columnar_extra_repair_registration
from .views import columnar_holiday_requests
from .views import columnar_single_holiday_requests
from .views import columnar_hr_change_date
from .views import columnar_hr_without_changer
from .views import columnar_hr_drive_loaded
from .views import columnar_shift_change_list
from .views import columnar_maintenance_schedule_menu
from .views import columnar_maintenance_schedule_auto
from .views import columnar_maintenance_schedule_ref

#chief column
from .views import chief_column_daily_report

#logist
from .views import logist_extra_repair
from .views import logist_holiday_requests
from .views import logist_holiday_request

#gate
from .views import gate_shift_change_list
from .views import gate_shift_change_single
from .views import gate_shift_change_inspection
from .views import gate_shift_change_inspection_1, gate_shift_change_inspection_2, gate_shift_change_inspection_3, gate_shift_change_inspection_4
from .views import gate_shift_change_inspection_5, gate_shift_change_inspection_6, gate_shift_change_inspection_7
from .views import gate_shift_change_complete

#insurance
from .views import insurance_trac_insurance
from .views import insurance_trailer_insurance

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
	
	#driver
	path('driver/extra-repair/', 	driver_extra_repair , name='driver_extra_repair'),
	path('driver/holiday-request/accept/', 	driver_hr_accept , name='driver_hr_accept'),
	path('driver/holiday-request/change_date/', 	driver_hr_change_date , name='driver_hr_change_date'),
	path('driver/holiday-request/without-changer/', 	driver_hr_without_changer , name='driver_hr_without_changer'),
	path('driver/holiday-request/drive-loaded/', 	driver_hr_drive_loaded , name='driver_hr_drive_loaded'),
	path('driver/holiday-requests/', 	driver_holiday_requests , name='driver_holiday_requests'),
	path('driver/new-holiday-request/', 	driver_new_holiday_request , name='driver_new_holiday_request'),
	path('driver/holiday-request/', 	driver_holiday_request , name='driver_holiday_request'),
	path('driver/shift-change/hand-over/acc/', 	driver_shift_change_hand_over_acc , name='driver_shift_change_hand_over_acc'),
	path('driver/shift-change/hand-over/', 	driver_shift_change_hand_over , name='driver_shift_change_hand_over'),
	path('driver/shift-change/accept-vehicle/accept/', 	driver_shift_change_accept_acc , name='driver_shift_change_accept_acc'),
	path('driver/shift-change/accept-vehicle/', 	driver_shift_change_accept , name='driver_shift_change_accept'),
	path('driver/shift-change/', 	driver_shift_change , name='driver_shift_change'),
	
	#columnar
	path('columnar/daily-report/', 	columnar_daily_report , name='columnar_daily_report'),
	path('columnar/extra-repair/registration/', 	columnar_extra_repair_registration , name='columnar_extra_repair_registration'),
	path('columnar/extra-repair/', 	columnar_extra_repair , name='columnar_extra_repair'),
	path('columnar/single-holiday-request/change_date/', 	columnar_hr_change_date , name='columnar_hr_change_date'),
	path('columnar/single-holiday-request/without-changer/', 	columnar_hr_without_changer , name='columnar_hr_without_changer'),
	path('columnar/single-holiday-request/drive-loaded/', 	columnar_hr_drive_loaded , name='columnar_hr_drive_loaded'),
	path('columnar/holiday-requests/', 	columnar_holiday_requests , name='columnar_holiday_requests'),
	path('columnar/single-holiday-request/', 	columnar_single_holiday_requests , name='columnar_single_holiday_requests'),
	path('columnar/shift-change/list/', 	columnar_shift_change_list , name='columnar_shift_change_list'),
	path('columnar/maintenance-schedule/menu/', 	columnar_maintenance_schedule_menu , name='columnar_maintenance_schedule_menu'),
	path('columnar/maintenance-schedule/auto/', 	columnar_maintenance_schedule_auto , name='columnar_maintenance_schedule_auto'),
	path('columnar/maintenance-schedule/ref/', 	columnar_maintenance_schedule_ref , name='columnar_maintenance_schedule_ref'),

	#chief column
	path('chief-column/daily-report/', 	chief_column_daily_report , name='chief_column_daily_report'),
	
	#logist
	path('logist/extra-repair/', 	logist_extra_repair , name='logist_extra_repair'),
	path('logist/holiday-requests/', 	logist_holiday_requests , name='logist_holiday_requests'),
	path('logist/holiday-request/', 	logist_holiday_request , name='logist_holiday_request'),

	#vorotny
	path('gate/shift-change/list/', 	gate_shift_change_list , name='gate_shift_change_list'),
	path('gate/shift-change/single/', 	gate_shift_change_single , name='gate_shift_change_single'),
	path('gate/shift-change/single/inspection/', 	gate_shift_change_inspection , name='gate_shift_change_inspection'),
	path('gate/shift-change/single/inspection/1/', 	gate_shift_change_inspection_1 , name='gate_shift_change_inspection_1'),
	path('gate/shift-change/single/inspection/2/', 	gate_shift_change_inspection_2 , name='gate_shift_change_inspection_2'),
	path('gate/shift-change/single/inspection/3/', 	gate_shift_change_inspection_3 , name='gate_shift_change_inspection_3'),
	path('gate/shift-change/single/inspection/4/', 	gate_shift_change_inspection_4 , name='gate_shift_change_inspection_4'),
	path('gate/shift-change/single/inspection/5/', 	gate_shift_change_inspection_5 , name='gate_shift_change_inspection_5'),
	path('gate/shift-change/single/inspection/6/', 	gate_shift_change_inspection_6 , name='gate_shift_change_inspection_6'),
	path('gate/shift-change/single/inspection/7/', 	gate_shift_change_inspection_7 , name='gate_shift_change_inspection_7'),
	path('gate/shift-change/single/complete/', 	gate_shift_change_complete , name='gate_shift_change_complete'),

	#insurance

	path('insurance/trac-insurance/', 	insurance_trac_insurance , name='insurance_trac_insurance'),
	path('insurance/trailer-insurance/', 	insurance_trailer_insurance , name='insurance_trailer_insurance'),
	
]
