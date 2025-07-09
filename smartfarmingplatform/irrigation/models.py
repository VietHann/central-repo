from django.db import models
from farms.models import Farm

class IrrigationSchedule(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    water_amount = models.FloatField()

    def __str__(self):
        return f'Irrigation Schedule for {self.farm.name}'