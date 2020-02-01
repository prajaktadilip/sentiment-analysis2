from django.db import models

class graph(models.Model):

    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()
# Create your models here.
