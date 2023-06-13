from django.contrib import admin
from django.urls import path
from .views import homepage

app_name = 'blog'


urlpatterns = [
    path('', homepage, name='homepage'),
]
