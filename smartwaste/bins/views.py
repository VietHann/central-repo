from django.shortcuts import render
from .models import Bin

def bin_list(request):
    bins = Bin.objects.all()
    return render(request, 'bins/bin_list.html', {'bins': bins})
