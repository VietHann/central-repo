from django.db import models
from bins.models import Bin

class Route(models.Model):
    name = models.CharField(max_length=200)
    bins = models.ManyToManyField(Bin)

    def __str__(self):
        return self.name
