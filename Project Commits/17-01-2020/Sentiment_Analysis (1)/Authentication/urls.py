from django.contrib import admin
from django.urls import path

from . import views

app_name = 'Authentication'

urlpatterns = [

    #path('signup',views.signup_view,name="signup"),
    path('',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),
    path('profile',views.profile,name="profile"),
    path('register/',views.register,name='register'),
]
