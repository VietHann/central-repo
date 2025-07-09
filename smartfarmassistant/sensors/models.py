from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f'{self.sensor.name} - {self.timestamp} - {self.value}'