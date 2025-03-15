from django.contrib import admin

# Register your models here.
from .models import Address
from .forms import AddressForm


class AddressAdmin(admin.ModelAdmin):
    model = Address
    form = AddressForm


admin.site.register(Address, AddressAdmin)