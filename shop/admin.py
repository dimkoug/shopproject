from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from core.actions import make_draft, make_published

from .models import (
    Category, ChildCategory, Tag,
    Supplier, WareHouse, Brand,
    BrandSupplier, Feature, FeatureCategory,
    Attribute, Product,
    ProductCategory, ProductTag, ProductRelated,
    Media, Logo, Stock, Shipment, ProductAttribute,
    Hero, HeroItem,
    Offer, OfferProduct, ShoppingCart,
    Address, Order, OrderItem,
)

from .forms import (
    CategoryForm, ChildCategoryForm, ChildCategoryFormSet,
    TagForm, SupplierForm, WareHouseForm, BrandForm,
    SupplierFormSet, FeatureForm, CategoryFormSet, AttributeForm,
    MediaFormSet, LogoFormSet, StockFormSet,
    ProductForm, ProductCategoryFormSet, ProductTagFormSet,
    ProductRelatedFormSet, MediaForm, LogoForm, StockForm, ShipmentForm,
    ProductAttributeFormSet, HeroForm, HeroItemFormSet, OfferForm,
    AddressForm, OrderForm, OrderItemFormSet,
    OfferProductForm, OfferProductFormSet
)


class ChildCategoryInline(admin.TabularInline):
    model = ChildCategory
    formset = ChildCategoryFormSet
    fk_name = 'source'
    extra = 1
    autocomplete_fields = ['target']



class SupplierInline(admin.TabularInline):
    model = BrandSupplier
    formset = SupplierFormSet
    fk_name = 'brand'
    extra = 1
    autocomplete_fields = ['supplier']


class CategoryInline(admin.TabularInline):
    model = FeatureCategory
    formset = CategoryFormSet
    fk_name = 'feature'
    extra = 1
    autocomplete_fields = ['category']


class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    formset = ProductCategoryFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['category']


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['tag']


class ProductRelatedInline(admin.TabularInline):
    model = ProductRelated
    formset = ProductRelatedFormSet
    fk_name = 'source'
    extra = 1
    autocomplete_fields = ['target']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['attribute']


class MediaInline(admin.TabularInline):
    model = Media
    formset = MediaFormSet
    fk_name = 'product'
    extra = 1


class LogoInline(admin.TabularInline):
    model = Logo
    formset = LogoFormSet
    fk_name = 'product'
    extra = 1



class StockInline(admin.TabularInline):
    model = Stock
    formset = StockFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['warehouse']


class HeroItemInline(admin.TabularInline):
    model = HeroItem
    formset = HeroItemFormSet
    fk_name = 'hero'
    extra = 1
    autocomplete_fields = ['product']



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    fk_name = 'order'


class BaseAdmin(admin.ModelAdmin):
    actions = [make_draft, make_published]


class CategoryAdmin(BaseAdmin):
    model = Category
    form = CategoryForm
    list_display = ('name', 'thumbnail', 'is_published', 'get_categories')
    search_fields = ['name']

    inlines = [
        ChildCategoryInline,
    ]

    def thumbnail(self, obj):
        try:
            return format_html('<img src="{}" style="width: 130px; \
                               height: 100px"/>'.format(obj.image.url))
        except:
            return ''

    thumbnail.short_description = 'thumbnail'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('children')
        return queryset

    def get_categories(self, obj):
        return "\n".join([p.name for p in obj.children.all()])


class TagAdmin(BaseAdmin):
    model = Tag
    form = TagForm
    list_display = ['name', 'is_published']
    search_fields = ['name']


class SupplierAdmin(BaseAdmin):
    model = Supplier
    form = SupplierForm
    list_display = ['name', 'is_published', 'get_brands']
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('brandsupplier_set')
        return queryset

    def get_brands(self, obj):
        return "\n".join([p.brand.name for p in obj.brandsupplier_set.all()])


class WareHouseAdmin(admin.ModelAdmin):
    model = WareHouse
    form = WareHouseForm
    search_fields = ['name']


class BrandAdmin(BaseAdmin):
    model = Brand
    form = BrandForm
    list_display = ['name', 'is_published', 'get_suppliers']

    inlines = [
        SupplierInline,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('brandsupplier_set')
        return queryset

    def get_suppliers(self, obj):
        return "\n".join([p.supplier.name for p in obj.brandsupplier_set.all()])


class FeatureAdmin(BaseAdmin):
    model = Feature
    form = FeatureForm
    search_fields = ['name']
    list_display = ['name', 'is_published', 'get_categories']

    inlines = [
        CategoryInline,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('featurecategory_set')
        return queryset

    def get_categories(self, obj):
        return "\n".join([p.category.name for p in obj.featurecategory_set.all()])


class AttributeAdmin(BaseAdmin):
    model = Attribute
    form = AttributeForm
    list_display = ('name', 'is_published', 'feature')
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('feature')
        return queryset



class ProductAdmin(BaseAdmin):
    model = Product
    form = ProductForm
    search_fields = ['name']
    list_display = ['name', 'brand', 'is_published']

    inlines = [
        ProductCategoryInline,
        ProductTagInline,
        ProductRelatedInline,
        ProductAttributeInline,
        MediaInline,
        LogoInline,
        StockInline
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('brand')
        return queryset


class MediaAdmin(BaseAdmin):
    model = Media
    form = MediaForm
    list_display = ['product', 'thumbnail', 'is_published']

    def thumbnail(self, obj):
        try:
            return format_html('<img src="{}" style="width: 130px; \
                               height: 100px"/>'.format(obj.image.url))
        except:
            return ''

    thumbnail.short_description = 'thumbnail'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class LogoAdmin(BaseAdmin):
    model = Logo
    form = LogoForm
    list_display = ['product', 'thumbnail', 'is_published']

    def thumbnail(self, obj):
        try:
            return format_html('<img src="{}" style="width: 130px; \
                               height: 100px"/>'.format(obj.image.url))
        except:
            return ''

    thumbnail.short_description = 'thumbnail'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset


class StockAdmin(admin.ModelAdmin):
    model = Stock
    form = StockForm


class ShipmentAdmin(admin.ModelAdmin):
    model = Shipment
    form = ShipmentForm


class HeroAdmin(BaseAdmin):
    model = Hero
    form = HeroForm
    list_display = ['name', 'is_published']

    inlines = [
        HeroItemInline,
    ]

class OfferProductInline(admin.TabularInline):
    model = OfferProduct
    extra = 1
    fk_name = 'offer'
    autocomplete_fields = ['product']


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm
    search_fields = ['name']

    inlines = [
        OfferProductInline
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
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Hero, HeroAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
