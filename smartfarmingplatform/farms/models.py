from django.db import models

class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    size = models.FloatField()

    def __str__(self):
        return self.name