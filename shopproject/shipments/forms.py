from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Shipment



class ShipmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ('warehouse', 'product', 'stock', 'date')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
