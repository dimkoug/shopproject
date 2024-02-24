from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet


from .models import WareHouse


class WareHouseForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = WareHouse
        fields = ('name',)