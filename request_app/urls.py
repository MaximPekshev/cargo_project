from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='request_index'),
    path('internal/', views.internal_index, name='internal_request_index'),
    path('external/', views.external_index, name='external_request_index'),
    path('external/search/<str:param>/', views.search, name='external_request_search'),
    path('external/order/<str:order>/', views.order, name = 'external_request_order'),
    # path('search/', views.searchRedir),
    path('external/search/', views.getAll, name = 'external_request_get_all'),
]