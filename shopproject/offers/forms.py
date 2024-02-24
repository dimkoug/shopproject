from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Offer, OfferProduct



class OfferForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'start_date', 'end_date')


class OfferProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = ('offer', 'product', 'is_complementary',
                  'is_primary', 'discount_price')


OfferProductFormSet = inlineformset_factory(Offer, OfferProduct,
                                            form=OfferProductForm,
                                            formset=BootstrapFormSet,
                                            can_delete=True,
                                            fk_name='offer')