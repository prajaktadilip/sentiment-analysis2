from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class fileupload(models.Model):
    filename = models.CharField(max_length=100)
    filetype = models.FileField(upload_to='filefolder')
    upload_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('Process:Analysis')


class Filedata(models.Model):
    filename = models.CharField(max_length=100)
    filetype = models.FileField(upload_to='filefolder')
    process_date = models.DateTimeField(default=timezone.now)
    
    positive = models.FloatField()
    negative = models.FloatField()
    neutral = models.FloatField()
    
    def __str__(self):
        return self.filename

    