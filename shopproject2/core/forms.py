from django import forms
from django.core.exceptions import ValidationError


class SlugValidator:
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        existing_objects = self.Meta.model.objects.filter(slug=slug)
        if self.instance:
            existing_objects = existing_objects.exclude(
                pk=self.instance.pk)
        if existing_objects:
            raise ValidationError('The slug already exists')
        return slug


class BootstrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
