from django.contrib import admin

# Register your models here.
from .models import (
    Category, ChildCategory, Tag,
    Supplier, WareHouse, Brand,
    BrandSupplier, Feature, FeatureCategory,
    Attribute, Product,
    ProductCategory, ProductTag, ProductRelated,
    Media, Logo, Stock, Shippment, ProductAttribute,
    Hero, HeroItem,
    Offer, OfferItem, ShoppingCartItem,
    Address, Order, OrderItem
)

from .forms import (
    CategoryForm, ChildCategoryForm, ChildCategoryFormSet,
    TagForm, SupplierForm, WareHouseForm, BrandForm,
    SupplierFormSet, FeatureForm, CategoryFormSet, AttributeForm,
    AttributeFormSet, MediaFormSet, LogoFormSet, StockFormSet,
    ProductForm, ProductCategoryFormSet, ProductTagFormSet,
    ProductRelatedFormSet, MediaForm, LogoForm, StockForm, ShippmentForm,
    ProductAttributeFormSet, HeroForm, HeroItemFormSet, OfferForm,
    OfferItemFormSet, AddressForm, OrderForm, OrderItemFormSet
)


class ChildCategoryInline(admin.TabularInline):
    model = ChildCategory
    formset = ChildCategoryFormSet
    fk_name = 'source'


class SupplierInline(admin.TabularInline):
    model = BrandSupplier
    formset = SupplierFormSet
    fk_name = 'brand'


class CategoryInline(admin.TabularInline):
    model = FeatureCategory
    formset = CategoryFormSet
    fk_name = 'feature'


class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    formset = ProductCategoryFormSet
    fk_name = 'product'


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet
    fk_name = 'product'


class ProductRelatedInline(admin.TabularInline):
    model = ProductRelated
    formset = ProductRelatedFormSet
    fk_name = 'source'


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet
    fk_name = 'product'


class MediaInline(admin.TabularInline):
    model = Media
    formset = MediaFormSet
    fk_name = 'product'


class LogoInline(admin.TabularInline):
    model = Logo
    formset = LogoFormSet
    fk_name = 'product'


class StockInline(admin.TabularInline):
    model = Stock
    formset = StockFormSet
    fk_name = 'product'


class HeroItemInline(admin.TabularInline):
    model = HeroItem
    formset = HeroItemFormSet
    fk_name = 'hero'


class OfferItemInline(admin.TabularInline):
    model = OfferItem
    formset = OfferItemFormSet
    fk_name = 'offer'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    fk_name = 'order'


class AttributeInline(admin.TabularInline):
    model = Attribute
    formset = AttributeFormSet
    fk_name = 'feature'


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm

    inlines = [
        ChildCategoryInline,
    ]


class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm


class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    form = SupplierForm


class WareHouseAdmin(admin.ModelAdmin):
    model = WareHouse
    form = WareHouseForm


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm

    inlines = [
        SupplierInline,
    ]


class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    form = FeatureForm

    inlines = [
        CategoryInline,
        AttributeInline,
    ]


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm


class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm

    inlines = [
        ProductCategoryInline,
        ProductTagInline,
        ProductRelatedInline,
        ProductAttributeInline,
        MediaInline,
        LogoInline,
        StockInline
    ]


class MediaAdmin(admin.ModelAdmin):
    model = Media
    form = MediaForm


class LogoAdmin(admin.ModelAdmin):
    model = Logo
    form = LogoForm


class StockAdmin(admin.ModelAdmin):
    model = Stock
    form = StockForm


class ShippmentAdmin(admin.ModelAdmin):
    model = Shippment
    form = ShippmentForm


class HeroAdmin(admin.ModelAdmin):
    model = Hero
    form = HeroForm

    inlines = [
        HeroItemInline,
    ]


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm

    inlines = [
        OfferItemInline,
    ]


class AddressAdmin(admin.ModelAdmin):
    model = Address
    form = AddressForm


class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = OrderForm

    inlines = [
        OrderItemInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(WareHouse, WareHouseAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Logo, LogoAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Shippment, ShippmentAdmin)
admin.site.register(Hero, HeroAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
