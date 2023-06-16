from django.contrib import admin
from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('new/', views.post_add, name='post_add'),
]
