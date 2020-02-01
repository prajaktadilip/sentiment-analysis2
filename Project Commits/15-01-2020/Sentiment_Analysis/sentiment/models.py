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
