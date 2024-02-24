from django.contrib import admin

# Register your models here.
from .models import Brand,BrandSupplier
from .forms import BrandForm,SupplierFormSet


class SupplierInline(admin.TabularInline):
    model = BrandSupplier
    formset = SupplierFormSet
    fk_name = 'brand'
    extra = 1
    autocomplete_fields = ['supplier']


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm

    inlines = [
        SupplierInline,
    ]


admin.site.register(Brand, BrandAdmin)