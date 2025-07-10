from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view()),
    path('mealplans/', views.MealPlanList.as_view()),
    path('mealplans/<int:pk>/', views.MealPlanDetail.as_view()),
]