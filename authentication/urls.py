from django.contrib import admin
from django.urls import path, include

from .views import *
urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name = 'register'),

    path('', user_logout, name = 'logout')
]