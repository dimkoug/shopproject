from django.contrib import admin

# Register your models here.
from .models import WareHouse
from .forms import WareHouseForm


class WareHouseAdmin(admin.ModelAdmin):
    model = WareHouse
    form = WareHouseForm
    search_fields = ['name']


admin.site.register(WareHouse, WareHouseAdmin)
