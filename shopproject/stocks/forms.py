from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet


from .models import Stock


class StockForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('warehouse', 'product', 'stock',)