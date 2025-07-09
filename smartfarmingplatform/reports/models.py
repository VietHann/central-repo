from django.db import models
from farms.models import Farm

class CropYield(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    date = models.DateField()
    yield_amount = models.FloatField()

    def __str__(self):
        return f'Crop Yield for {self.farm.name} on {self.date}'