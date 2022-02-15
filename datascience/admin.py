from django.contrib import admin
from .models import Customer, Product, Position, Sale, CSV, Report

# Register your models here.

admin.register(Customer, Product, Position, Sale, CSV, Report)(admin.ModelAdmin)