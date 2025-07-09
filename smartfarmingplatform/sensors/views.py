from django.shortcuts import render

def sensor_list(request):
    return render(request, 'sensors/sensor_list.html')