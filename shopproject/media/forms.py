from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from media.models import Media

class MediaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Media
        fields = ('image', 'image_url', 'is_published', 'order')