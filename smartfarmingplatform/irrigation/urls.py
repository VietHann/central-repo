from django.urls import path
from . import views

urlpatterns = [
    path('', views.irrigation_list, name='irrigation_list'),
]