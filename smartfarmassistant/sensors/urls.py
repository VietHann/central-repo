from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.SensorList.as_view()),
    path('sensors/<int:pk>/', views.SensorDetail.as_view()),
    path('sensor_data/', views.SensorDataList.as_view()),
    path('sensor_data/<int:pk>/', views.SensorDataDetail.as_view()),
]