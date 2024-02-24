from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Hero, HeroItem


class HeroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('name', 'is_published', 'order')


class HeroItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = HeroItem
        fields = ('hero', 'product')


HeroItemFormSet = inlineformset_factory(Hero, HeroItem,
                                        form=HeroItemForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='hero')