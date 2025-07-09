from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.DeviceList.as_view()),
    path('devices/<int:pk>/', views.DeviceDetail.as_view()),
]