from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm
from .models import (Category, Tag, Specification, Attribute,Product,ProductTag,
                     ProductShipment,
                     ProductAttribute,ProductCategory,
                     Brand,ProductMedia)

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

class CategoryForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug', 'meta_description',
                  'meta_keywords', 'image','is_published')

class TagForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published')


class ProductMediaForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ('product', 'caption', 'image', 'is_published')

class ProductShipmentForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductShipment
        fields = ('product', 'stock','shipment_date')


class BrandForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name','slug', 'image', 'is_published')


class SpecificationForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Specification
        fields = ('name', 'category', 'is_published')


class AttributeForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', 'specification')


class ProductForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'parent', 'brand', 'slug','price',
                  'description',
                  'meta_description', 'meta_keywords','image', 'featured', 'is_published')

class ProductTagForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = ('product', 'tag')


class ProductAttributeForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('product', 'attribute')

class ProductCategoryForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('product', 'category')



ProductCategoryFormSet = inlineformset_factory(Product,ProductCategory,
                                          formset=unique_field_formset('category'),
                                          form=ProductCategoryForm)

ProductTagFormSet = inlineformset_factory(Product,ProductTag,
                                          formset=unique_field_formset('tag'),
                                          form=ProductTagForm)
ProductAttributeFormSet = inlineformset_factory(Product,ProductAttribute,
                                                formset=unique_field_formset('attribute'),
                                                form=ProductAttributeForm)

ProductMediaFormSet = inlineformset_factory(Product,ProductMedia,
                                            form=ProductMediaForm)
