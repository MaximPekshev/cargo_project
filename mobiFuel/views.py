from django.shortcuts import redirect, render

def index(request):
    if request.user.is_authenticated:
        gosNumber = request.GET.get('gosNumber')
        gasStation = request.GET.get('gasStation')
        if gasStation:
            gasStation = gasStation.split(',')
        # print(gosNumber)
        # print(gasStation)
        
        return render(request, 'mobiFuel/index.html',{'count':range(300)})
    return redirect('/admin/')