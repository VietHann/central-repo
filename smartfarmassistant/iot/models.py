from django.db import models
from farms.models import Farm

class Device(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)
    status = models.BooleanField(default=False) # e.g., True for ON, False for OFF

    def __str__(self):
        return self.name
