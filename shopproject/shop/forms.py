from django import forms
from django.forms import inlineformset_factory
from adminsortable2.admin import CustomInlineFormSet
from core.forms import (BootstrapForm, CoreBaseForm, AdminImageWidget,
                        unique_field_formset, ShortableFormSet)
from .models import (Category, Tag, Specification, Attribute, Product,
                     ProductTag, ProductShipment, Supplier, BrandSupplier,
                     ProductAttribute, ProductCategory,
                     Brand, ProductMedia, Offer, OfferDetail, Order,
                     OrderDetail, Hero, HeroItem)


class OrderForm(CoreBaseForm):
    class Meta:
        model = Order
        fields = ('profile',)
        widgets = {'profile': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile'].initial = self.request.user.profile.pk


class OrderDetailForm(CoreBaseForm):
    class Meta:
        model = OrderDetail
        fields = ('order', 'product', 'quantity')


class OfferForm(CoreBaseForm):
    class Meta:
        model = Offer
        fields = ('name', 'start_date', 'end_date', 'is_published')


class OfferDetailForm(CoreBaseForm):
    class Meta:
        model = OfferDetail
        fields = ('offer', 'product', 'price')


class CategoryForm(CoreBaseForm):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug', 'meta_description',
                  'meta_keywords', 'image', 'is_published', 'is_featured')
        widgets = {
            'image': AdminImageWidget,
        }


class TagForm(CoreBaseForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published')


class HeroForm(CoreBaseForm):
    class Meta:
        model = Hero
        fields = ('name', 'is_published')


class HeroItemForm(CoreBaseForm):
    class Meta:
        model = HeroItem
        fields = ('hero', 'product', 'is_published')


class SupplierForm(CoreBaseForm):
    class Meta:
        model = Supplier
        fields = ('name',)


class ProductMediaForm(CoreBaseForm):
    class Meta:
        model = ProductMedia
        fields = ('product', 'caption', 'image', 'is_published')
        widgets = {
            'image': AdminImageWidget,
        }


class ProductShipmentForm(CoreBaseForm):
    class Meta:
        model = ProductShipment
        fields = ('product', 'stock', 'shipment_date')


class BrandForm(CoreBaseForm):
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'suppliers', 'image', 'is_published')
        widgets = {
            'image': AdminImageWidget,
        }


class SpecificationForm(CoreBaseForm):
    class Meta:
        model = Specification
        fields = ('name', 'categories', 'is_published')


class AttributeForm(CoreBaseForm):
    class Meta:
        model = Attribute
        fields = ('name', 'specification')


class ProductForm(CoreBaseForm):
    class Meta:
        model = Product
        fields = ('name', 'parent', 'brand', 'slug', 'price',
                  'description', 'categories', 'tags', 'attributes',
                  'meta_description', 'meta_keywords', 'image',
                  'featured', 'is_published')
        widgets = {
            'image': AdminImageWidget,
        }


class ProductTagForm(CoreBaseForm):
    class Meta:
        model = ProductTag
        fields = ('product', 'tag')


class ProductAttributeForm(CoreBaseForm):
    class Meta:
        model = ProductAttribute
        fields = ('product', 'attribute')


class ProductCategoryForm(CoreBaseForm):
    class Meta:
        model = ProductCategory
        fields = ('product', 'category')


class BrandSupplierForm(CoreBaseForm):
    class Meta:
        model = BrandSupplier
        fields = ('brand', 'supplier')


BrandSupplierFormSet = inlineformset_factory(
    Brand, BrandSupplier, formset=unique_field_formset('supplier'),
    form=BrandSupplierForm, can_delete=True,
    can_order=True
)


ProductCategoryFormSet = inlineformset_factory(
    Product, ProductCategory, formset=unique_field_formset('category'),
    form=ProductCategoryForm, can_delete=True,
    can_order=True
)

ProductTagFormSet = inlineformset_factory(
    Product, ProductTag, formset=unique_field_formset('tag'),
    form=ProductTagForm, can_delete=True,
    can_order=True
)

ProductAttributeFormSet = inlineformset_factory(
    Product, ProductAttribute,
    formset=unique_field_formset('attribute'),
    form=ProductAttributeForm, can_delete=True,
    can_order=True
)

ProductMediaFormSet = inlineformset_factory(
    Product, ProductMedia, form=ProductMediaForm,
    formset=ShortableFormSet, can_delete=True,
    can_order=True
)
