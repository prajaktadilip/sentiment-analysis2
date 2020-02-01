from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
class fileupload(models.Model):
    filename = models.CharField(max_length=100)
    filetype = models.FileField(upload_to='filefolder')
    upload_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('home')


class overall_rating1(models.Model):
    filename = models.CharField(max_length=100)
    process_date = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=0.0)
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()
    
    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('filehome')
