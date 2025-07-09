from django.urls import path
from . import views

urlpatterns = [
    path('farms/', views.FarmList.as_view()),
    path('farms/<int:pk>/', views.FarmDetail.as_view()),
    path('crops/', views.CropList.as_view()),
    path('crops/<int:pk>/', views.CropDetail.as_view()),
]