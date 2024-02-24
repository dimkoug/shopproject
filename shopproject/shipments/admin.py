from django.contrib import admin

# Register your models here.

from .models import Shipment
from .forms import ShipmentForm


class ShipmentAdmin(admin.ModelAdmin):
    model = Shipment
    form = ShipmentForm




admin.site.register(Shipment, ShipmentAdmin)


