# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chat/', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
]