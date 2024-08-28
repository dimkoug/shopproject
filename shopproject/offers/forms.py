from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Offer, OfferProduct



class OfferForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class OfferProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = ('offer', 'product', 'is_complementary',
                  'is_primary', 'discount_price')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


