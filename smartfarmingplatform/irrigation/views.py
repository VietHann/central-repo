from django.shortcuts import render

def irrigation_list(request):
    return render(request, 'irrigation/irrigation_list.html')