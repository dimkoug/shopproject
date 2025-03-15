from django import forms
from django.forms import inlineformset_factory

from core.widgets import *
from core.forms import BootstrapForm, BootstrapFormSet

from products.models import Product

from offers.models import Offer, OfferProduct



class OfferForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class OfferProductForm(BootstrapForm, forms.ModelForm):
    product = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/shop/products/sb/'),required=False,queryset=Product.objects.none())
    class Meta:
        model = OfferProduct
        fields = ('offer', 'product', 'is_complementary',
                  'is_primary', 'discount_price')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        products_queryset = Product.objects.none()
        if 'offer' in self.initial:
            self.fields['offer'].widget = forms.HiddenInput()

        if 'product' in self.data:
            products_queryset = Product.objects.all()


        if self.instance.pk:
            products_queryset = Product.objects.filter(id=self.instance.product_id)

        self.fields['product'].queryset = products_queryset
        self.fields['product'].widget.queryset = products_queryset


