from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import (
    Category, ChildCategory, Tag, Supplier, WareHouse, Brand,
    BrandSupplier, Feature, FeatureCategory, Attribute, Product,
    ProductCategory, ProductTag, ProductRelated, Media, Logo, Stock,
    Shippment, ProductAttribute, Hero, HeroItem,
    Offer, OfferItem, Address, Order, OrderItem
)


class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'url', 'image', 'is_published', 'order')


class ChildCategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ChildCategory
        fields = ('source', 'target', 'is_published', 'order')


ChildCategoryFormSet = inlineformset_factory(Category, ChildCategory,
                                             form=ChildCategoryForm,
                                             formset=BootstrapFormSet,
                                             can_delete=True,
                                             fk_name='source')


class TagForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'is_published', 'order')


class SupplierForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'is_published', 'order')


class WareHouseForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = WareHouse
        fields = ('name', 'is_published', 'order')


class BrandForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'image', 'is_published', 'order')


class BrandSupplierForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = BrandSupplier
        fields = ('brand', 'supplier', 'is_published', 'order')


SupplierFormSet = inlineformset_factory(Brand, BrandSupplier,
                                        form=BrandSupplierForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='brand')


class FeatureForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'image', 'is_published', 'order')


class FeatureCategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = FeatureCategory
        fields = ('feature', 'category', 'is_published', 'order')


CategoryFormSet = inlineformset_factory(Feature, FeatureCategory,
                                        form=FeatureCategoryForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='feature')


class AttributeForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', 'feature', 'is_published', 'order')


AttributeFormSet = inlineformset_factory(Feature, Attribute,
                                         form=AttributeForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='feature')


class ProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'brand', 'parent', 'image', 'subtitle',
                  'description', 'price', 'is_published', 'order')


class ProductCategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('product', 'category', 'is_published', 'order')


ProductCategoryFormSet = inlineformset_factory(Product, ProductCategory,
                                               form=ProductCategoryForm,
                                               formset=BootstrapFormSet,
                                               can_delete=True,
                                               fk_name='product')


class ProductTagForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = ('product', 'tag', 'is_published', 'order')


ProductTagFormSet = inlineformset_factory(Product, ProductTag,
                                          form=ProductTagForm,
                                          formset=BootstrapFormSet,
                                          can_delete=True,
                                          fk_name='product')


class ProductRelatedForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductRelated
        fields = ('source', 'target', 'is_published', 'order')


ProductRelatedFormSet = inlineformset_factory(Product, ProductRelated,
                                              form=ProductRelatedForm,
                                              formset=BootstrapFormSet,
                                              can_delete=True,
                                              fk_name='source')


class MediaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Media
        fields = ('product', 'image', 'is_published', 'order')


MediaFormSet = inlineformset_factory(Product, Media,
                                     form=MediaForm,
                                     formset=BootstrapFormSet,
                                     can_delete=True,
                                     fk_name='product')


class LogoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Logo
        fields = ('product', 'image', 'is_published', 'order')


LogoFormSet = inlineformset_factory(Product, Logo,
                                    form=MediaForm,
                                    formset=BootstrapFormSet,
                                    can_delete=True,
                                    fk_name='product')


class StockForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Stock
        fields = ('warehouse', 'product', 'stock', 'is_published', 'order')


StockFormSet = inlineformset_factory(Product, Stock,
                                     form=StockForm,
                                     formset=BootstrapFormSet,
                                     can_delete=True,
                                     fk_name='product')


class ShippmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Shippment
        fields = ('warehouse', 'product', 'stock', 'date',
                  'is_published', 'order')


class ProductAttributeForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('attribute', 'product', 'is_published', 'order')


ProductAttributeFormSet = inlineformset_factory(Product, ProductAttribute,
                                                form=ProductAttributeForm,
                                                formset=BootstrapFormSet,
                                                can_delete=True,
                                                fk_name='product')


class HeroForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('name', 'is_published', 'order')


class HeroItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = HeroItem
        fields = ('hero', 'product', 'is_published', 'order')


HeroItemFormSet = inlineformset_factory(Hero, HeroItem,
                                        form=HeroItemForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='hero')


class OfferForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'start_date', 'end_date', 'is_published', 'order')


class OfferItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OfferItem
        fields = ('offer', 'product', 'price',  'is_published', 'order')


OfferItemFormSet = inlineformset_factory(Offer, OfferItem,
                                         form=OfferItemForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='offer')


class AddressForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = ('profile', 'address_type',  'first_name', 'last_name',
                  'mobile', 'street_name', 'postal_code', 'city',
                  'street_number', 'floor_number')


class OrderForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_registration', 'billing_address', 'shipping_address',
                  'total', 'comments')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class OrderItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity')


OrderItemFormSet = inlineformset_factory(Order, OrderItem,
                                         form=OrderItemForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='order')
