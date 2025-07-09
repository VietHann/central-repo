from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    size = models.FloatField()

    def __str__(self):
        return self.name

class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    planting_date = models.DateField()

    def __str__(self):
        return self.name