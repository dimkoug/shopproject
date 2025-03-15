from django.contrib import admin

# Register your models here.
from .models import *
from .forms import BrandForm


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm

admin.site.register(Brand, BrandAdmin)