from django.shortcuts import render

def farm_list(request):
    return render(request, 'farms/farm_list.html')