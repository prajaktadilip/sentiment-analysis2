from django.contrib import admin
from django.urls import path
from .views import (
    fileListView,
    fileDetailView,
    fileCreateView,
    UserFileListView
)

from . import views

app_name = 'Process'

urlpatterns = [

    path('homepage',views.home_page,name="homepage"),
    path('about',views.about,name="About"),
    path('Analysis',views.Analysis,name="Analysis"),
    path('fileupload/',fileCreateView.as_view(),name='fileupload'),
    path('piechart',views.piechart,name="piechart"),
    path('Individual',views.Individual,name="Individual"),
    
    
   
]
