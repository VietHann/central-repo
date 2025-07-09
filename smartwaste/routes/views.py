from django.shortcuts import render
from .models import Route

def route_list(request):
    routes = Route.objects.all()
    return render(request, 'routes/route_list.html', {'routes': routes})
