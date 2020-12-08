from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, AdminImageWidget, unique_field_formset
from .models import (Category, Tag, Specification, Attribute,Product,ProductTag,
                     ProductShipment,
                     Supplier, BrandSupplier,
                     ProductAttribute,ProductCategory,
                     Brand,ProductMedia)



class CategoryForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug', 'meta_description',
                  'meta_keywords', 'image','is_published')
        widgets = {
            'image': AdminImageWidget,
        }

class TagForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published')


class SupplierForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name',)


class ProductMediaForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ('product', 'caption', 'image', 'is_published')
        widgets = {
            'image': AdminImageWidget,
        }


class ProductShipmentForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = ProductShipment
        fields = ('product', 'stock','shipment_date')


class BrandForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name','slug', 'image', 'is_published')
        widgets = {
            'image': AdminImageWidget,
        }


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
        widgets = {
            'image': AdminImageWidget,
        }

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


class BrandSupplierForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = BrandSupplier
        fields = ('brand', 'supplier')



BrandSupplierFormSet = inlineformset_factory(Brand,BrandSupplier,
                                          formset=unique_field_formset('supplier'),
                                          form=BrandSupplierForm)


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
