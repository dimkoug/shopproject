from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from .models import (
    Category, ChildCategory, Tag, Supplier, WareHouse, Brand,
    BrandSupplier, Feature, FeatureCategory, Attribute, Product,
    ProductTag, ProductRelated, Media, Logo, Stock,
    Shipment, ProductAttribute, Hero, HeroItem,
    Offer, Address, Order, OrderItem,
    OfferProduct
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
        fields = ('name', 'is_published', 'feature', 'order')


AttributeFormSet = inlineformset_factory(Feature, Attribute,
                                         form=AttributeForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='feature')


class ProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'brand','category', 'parent', 'image', 'subtitle',
                  'description', 'price', 'is_published', 'order')


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


class ShipmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Shipment
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
        fields = ('name', 'start_date', 'end_date')


class OfferProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = ('offer', 'product', 'is_complementary', 'is_primary', 'discount_price')


OfferProductFormSet = inlineformset_factory(Offer, OfferProduct,
                                            form=OfferProductForm,
                                            formset=BootstrapFormSet,
                                            can_delete=True,
                                            fk_name='offer')




class AddressForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = ('profile', 'address_type',  'first_name', 'last_name',
                  'mobile', 'street_name', 'postal_code', 'city',
                  'street_number', 'floor_number')


class SiteAddressForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Address
        fields = ('first_name', 'last_name',
                  'mobile', 'street_name', 'postal_code', 'city',
                  'street_number', 'floor_number')


class OrderForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_registration', 'billing_address', 'shipping_address',
                  'total', 'comments')

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop("request")
        except KeyError:
            pass
        super().__init__(*args, **kwargs)


class SiteOrderForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('billing_address', 'shipping_address',
                  'comments')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['billing_address'].queryset = Address.objects.select_related(
            'profile').filter(profile_id=self.request.user.profile.pk,
                              address_type=Address.BILLING_ADDRESS)
        self.fields['shipping_address'].queryset = Address.objects.select_related(
            'profile').filter(profile_id=self.request.user.profile.pk,
                              address_type=Address.SHIPPING_ADDRESS)




class OrderItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity')


OrderItemFormSet = inlineformset_factory(Order, OrderItem,
                                         form=OrderItemForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='order')
