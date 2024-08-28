from django.contrib import admin

# Register your models here.
from .models import Warehouse
from .forms import WarehouseForm


class WarehouseAdmin(admin.ModelAdmin):
    model = Warehouse
    form = WarehouseForm
    search_fields = ['name']


admin.site.register(Warehouse, WarehouseAdmin)
