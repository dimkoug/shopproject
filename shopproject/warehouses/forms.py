from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet


from warehouses.models import Warehouse


class WarehouseForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)