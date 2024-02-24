from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Address


class AddressForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = ('profile', 'address_type',  'first_name', 'last_name',
                  'mobile', 'street_name', 'postal_code', 'city',
                  'street_number', 'floor_number')


class SiteAddressForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name',
                  'mobile', 'street_name', 'postal_code', 'city',
                  'street_number', 'floor_number')