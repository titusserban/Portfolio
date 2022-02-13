from django.urls import path
from openweatherapi import views

app_name = "openweatherapi"

urlpatterns = [
    path('', views.openweather, name="openweather"),
]