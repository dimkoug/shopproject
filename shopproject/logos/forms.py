from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Logo

class LogoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Logo
        fields = ('image', 'is_published', 'order')