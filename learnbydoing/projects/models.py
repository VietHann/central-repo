from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.TextField()
    code_explanation = models.TextField()

    def __str__(self):
        return self.title