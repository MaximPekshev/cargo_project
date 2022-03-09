from django.urls import path
from .views import upload_autograph_data
from .views import show_autograph_upload_menu

urlpatterns = [
	# path('', 	show_autograph_page , name='show_autograph_page'),
	path('upload/<str:input_date>/', 	upload_autograph_data , name='upload_autograph_data'),
	path('upload/', 	show_autograph_upload_menu , name='show_autograph_upload_menu'),
]