from django.db import models
from bins.models import Bin

class SensorData(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.FloatField()

    def __str__(self):
        return f'Sensor data for bin {self.bin} at {self.timestamp}'
