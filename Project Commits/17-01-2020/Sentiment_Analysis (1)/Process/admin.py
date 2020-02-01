from django.contrib import admin

# Register your models here.
from .models import fileupload,Filedata

admin.site.register(fileupload)
admin.site.register(Filedata)