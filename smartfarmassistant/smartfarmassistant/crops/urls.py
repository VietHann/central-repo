from django.urls import path
from . import views

urlpatterns = [
    path('', views.CropListCreate.as_view()),
    path('<int:pk>/', views.CropRetrieveUpdateDestroy.as_view()),
]