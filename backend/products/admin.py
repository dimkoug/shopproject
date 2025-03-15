
from django.contrib import admin
from products.models import *  # Adjust the import path if necessary

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Add relevant fields for searching