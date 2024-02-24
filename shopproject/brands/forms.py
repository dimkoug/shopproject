from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import Brand,BrandSupplier


class BrandForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'image', 'suppliers', 'is_published', 'order')


class BrandSupplierForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = BrandSupplier
        fields = ('brand', 'supplier',)


SupplierFormSet = inlineformset_factory(Brand, BrandSupplier,
                                        form=BrandSupplierForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='brand')