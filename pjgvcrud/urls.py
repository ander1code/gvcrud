from django.contrib import admin
from django.urls import path, include
from gvcrud import views

urlpatterns = [
    path('', include('gvcrud.urls')),
    path('login/', views.login_auth, name='login-auth'),
    path('logoff/', views.logoff, name='logoff')
]
