from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Logo

class LogoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Logo
        fields = ('image', 'image_url', 'is_published', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)