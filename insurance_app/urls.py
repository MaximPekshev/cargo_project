from django.urls import path
from .views import insurance_trac_insurance, insurance_trailer_insurance

urlpatterns = [
    path('trac-insurance/', 	insurance_trac_insurance , name='insurance_trac_insurance'),
	path('trailer-insurance/', 	insurance_trailer_insurance , name='insurance_trailer_insurance'),
]
