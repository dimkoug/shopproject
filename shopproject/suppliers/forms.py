from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Supplier



class SupplierForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'is_published', 'order')