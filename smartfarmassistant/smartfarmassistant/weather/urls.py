from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeatherDataListCreate.as_view()),
    path('<int:pk>/', views.WeatherDataRetrieveUpdateDestroy.as_view()),
]