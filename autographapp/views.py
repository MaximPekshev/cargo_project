from django.shortcuts import render, redirect
from cargoapp.models import Vehicle
from autographapp.models import AutographDailyIndicators
import datetime

# def show_autograph_page(request):
#     if request.user.is_authenticated:
#         yesterday = datetime.datetime.now() -  datetime.timedelta(days=5)
#         context = {
#             'vehicles' : AutographDailyIndicators.objects.filter(date=yesterday, vehicle__in=Vehicle.objects.all()),
#             'date' : yesterday,
#         }
#         return render(request, 'autographapp/autograph.html', context)
#     else:
#         return redirect('login')