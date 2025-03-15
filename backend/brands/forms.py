from django import forms

from core.forms import BootstrapForm


from brands.models import Brand

class BrandForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'image',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

