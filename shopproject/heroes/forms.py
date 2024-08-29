from django import forms
from django.forms import inlineformset_factory
from core.widgets import *
from core.forms import BootstrapForm, BootstrapFormSet

from shop.models import Product

from heroes.models import Hero, HeroItem


class HeroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('name', 'is_published', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class HeroItemForm(BootstrapForm, forms.ModelForm):
    product = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/shop/products/sb/'),required=False,queryset=Product.objects.none())
    class Meta:
        model = HeroItem
        fields = ('hero', 'product')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        products_queryset = Product.objects.none()
        if 'hero' in self.initial:
            self.fields['hero'].widget = forms.HiddenInput()

        if 'product' in self.data:
            products_queryset = Product.objects.all()


        if self.instance.pk:
            products_queryset = Product.objects.filter(id=self.instance.product_id)

        self.fields['product'].queryset = products_queryset
        self.fields['product'].widget.queryset = products_queryset
        


