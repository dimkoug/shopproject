from django.contrib import admin

# Register your models here.
from .models import Supplier
from .forms import SupplierForm

class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    form = SupplierForm
    search_fields = ['name']


admin.site.register(Supplier, SupplierAdmin)