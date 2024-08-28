from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Hero, HeroItem


class HeroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('name', 'is_published', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class HeroItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = HeroItem
        fields = ('hero', 'product')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


