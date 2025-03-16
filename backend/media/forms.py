from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from media.models import Media

class MediaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Media
        fields = ('image', 'url', 'is_published')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)