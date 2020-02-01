from django import forms
from django.contrib.auth.models import User
from .models import fileupload,Filedata

class fileUploadForm(forms.ModelForm):
    
    class Meta:
        model = fileupload
        fields = ['filename','filetype']


class File_data(forms.ModelForm):
	class Meta:
		model=Filedata
		fields = ['filename','filetype','positive','negative','neutral']
