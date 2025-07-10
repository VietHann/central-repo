from django.contrib import admin
from .models import Recipe, MealPlan

admin.site.register(Recipe)
admin.site.register(MealPlan)