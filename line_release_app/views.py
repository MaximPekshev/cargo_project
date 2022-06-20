from django.shortcuts import render

def show_line_release_list(request):
    
    return render(request, 'line_release_app/line_release_list.html')
