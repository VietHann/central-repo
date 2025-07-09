from django.db import models
from farms.models import Farm

class Sensor(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sensor_type} - {self.value}'