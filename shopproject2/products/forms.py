from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm
from .models import (Category, Tag, Feature, Attribute,Product,ProductTag,
                     ProductAttribute, Order, Brand)

def unique_field_formset(field_name):
    from django.forms.models import BaseInlineFormSet
    class UniqueFieldFormSet(BaseInlineFormSet):
        def clean(self):
            if any(self.errors):
                # Don't bother validating the formset unless each form is valid on its own
                return
            values = set()
            for form in self.forms:
                if form.cleaned_data:
                    value = form.cleaned_data[field_name]
                    if value in values:
                        raise forms.ValidationError('Duplicate values for "%s" are not allowed.' % field_name)
                    values.add(value)
    return UniqueFieldFormSet


class OrderForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Order
        fields = ('profile', 'amount')
        widgets = {'amount': forms.HiddenInput(), 'profile': forms.HiddenInput()}


class CategoryForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug', 'meta_description',
                  'meta_keywords', 'is_published')

class TagForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published')


class BrandForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'is_published')


class FeatureForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'category', 'is_published')


class AttributeForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', 'feature')


class ProductForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'parent', 'brand', 'category', 'slug','price',
                  'meta_description', 'meta_keywords', 'is_published')

class ProductTagForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = ('product', 'tag')


class ProductAttributeForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('product', 'attribute')

ProductTagFormSet = inlineformset_factory(Product,ProductTag,
                                          formset=unique_field_formset('tag'),
                                          form=ProductTagForm)
ProductAttributeFormSet = inlineformset_factory(Product,ProductAttribute,
                                                formset=unique_field_formset('attribute'),
                                                form=ProductAttributeForm)
