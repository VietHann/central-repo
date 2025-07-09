from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    planting_date = models.DateField()
    age = models.IntegerField()

    def __str__(self):
        return self.name