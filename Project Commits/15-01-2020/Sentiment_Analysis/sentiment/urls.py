from django.urls import path, include
from . import views
from .views import (
    fileListView,
    fileDetailView,
    fileCreateView,
    UserFileListView
)

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('fileupload/',fileCreateView.as_view(),name='fileupload'),
    path('filelist/',fileListView.as_view(),name='filelist'),
    path('filelist/user/<str:username>',UserFileListView.as_view(),name='user-fileupload'),
    path('sen/',views.about,name='sen')
]

