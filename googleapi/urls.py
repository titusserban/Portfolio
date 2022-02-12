from django.urls import path
from googleapi import views

app_name = "googleapi"

urlpatterns = [
    path('', views.Route.as_view(), name="route"),
    path('map', views.map, name="map"),
]