from django.contrib import admin
from django.urls import path
from .views import pulsar

urlpatterns = [
    path('', pulsar, name='pulsar'),
]

