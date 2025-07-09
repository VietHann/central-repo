from django.db import models

class WeatherData(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    light_intensity = models.FloatField()

    def __str__(self):
        return str(self.date)