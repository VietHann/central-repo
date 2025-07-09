from django.db import models

class Bin(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    capacity = models.FloatField()
    current_level = models.FloatField()

    def __str__(self):
        return f'Bin at ({self.latitude}, {self.longitude})'
