from django.db import models

# Example models (replace with your actual models)
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    calories = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    date = models.DateField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.recipe.name}'