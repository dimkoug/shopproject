from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Shipment



class ShipmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ('warehouse', 'product', 'stock', 'date')
