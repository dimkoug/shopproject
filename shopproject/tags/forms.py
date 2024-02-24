from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Tag


class TagForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published', 'order')