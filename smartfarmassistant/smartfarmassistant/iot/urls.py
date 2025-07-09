from django.urls import path
from . import views

urlpatterns = [
    path('', views.SensorDataListCreate.as_view()),
    path('<int:pk>/', views.SensorDataRetrieveUpdateDestroy.as_view()),
]