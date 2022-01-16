from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
# Register your models here.

from core.actions import make_draft, make_published

from .models import (
    Category, ChildCategory, Tag,
    Supplier, WareHouse, Brand,
    BrandSupplier, Feature, FeatureCategory,
    Attribute, Product,
    ProductTag, ProductRelated,
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
    ProductForm, ProductTagFormSet,
    ProductRelatedFormSet, MediaForm, LogoForm, StockForm, ShipmentForm,
    ProductAttributeFormSet, HeroForm, HeroItemFormSet, OfferForm,
    AddressForm, OrderForm, OrderItemFormSet,
    OfferProductForm, OfferProductFormSet
)


class ChildCategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Category.children.through
    fk_name = 'source'
    extra = 1
    autocomplete_fields = ['target']



class SupplierInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BrandSupplier
    formset = SupplierFormSet
    fk_name = 'brand'
    extra = 1
    autocomplete_fields = ['supplier']


class CategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = FeatureCategory
    formset = CategoryFormSet
    fk_name = 'feature'
    extra = 1
    autocomplete_fields = ['category']



class ProductTagInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['tag']


class ProductRelatedInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductRelated
    formset = ProductRelatedFormSet
    fk_name = 'source'
    extra = 1
    autocomplete_fields = ['target']


class ProductAttributeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['attribute']


class MediaInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Media
    formset = MediaFormSet
    fk_name = 'product'
    extra = 1


class LogoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Logo
    formset = LogoFormSet
    fk_name = 'product'
    extra = 1



class StockInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Stock
    formset = StockFormSet
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['warehouse']


class HeroItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = HeroItem
    formset = HeroItemFormSet
    fk_name = 'hero'
    extra = 1
    autocomplete_fields = ['product']



class OrderItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    fk_name = 'order'


class BaseAdmin(admin.ModelAdmin):
    actions = [make_draft, make_published]


class CategoryAdmin(SortableAdminMixin, BaseAdmin):
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


class TagAdmin(SortableAdminMixin, BaseAdmin):
    model = Tag
    form = TagForm
    list_display = ['name', 'is_published']
    search_fields = ['name']


class SupplierAdmin(SortableAdminMixin, BaseAdmin):
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


class WareHouseAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = WareHouse
    form = WareHouseForm
    search_fields = ['name']


class BrandAdmin(SortableAdminMixin, BaseAdmin):
    model = Brand
    form = BrandForm
    search_fields = ['name']
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


class FeatureAdmin(SortableAdminMixin, BaseAdmin):
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


class AttributeAdmin(SortableAdminMixin, BaseAdmin):
    model = Attribute
    form = AttributeForm
    list_display = ('name', 'is_published', 'feature')
    search_fields = ['name']
    autocomplete_fields = ['feature']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('feature')
        return queryset



class ProductAdmin(SortableAdminMixin, BaseAdmin):
    model = Product
    form = ProductForm
    search_fields = ['name']
    list_display = ['name', 'parent', 'brand', 'category', 'is_published']
    autocomplete_fields = ['brand', 'parent', 'category']

    inlines = [
        ProductTagInline,
        ProductRelatedInline,
        ProductAttributeInline,
        MediaInline,
        LogoInline,
        StockInline
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('brand', 'category')
        return queryset


class MediaAdmin(SortableAdminMixin, BaseAdmin):
    model = Media
    form = MediaForm
    list_display = ['product', 'thumbnail', 'is_published']
    autocomplete_fields = ['product']

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


class LogoAdmin(SortableAdminMixin, BaseAdmin):
    model = Logo
    form = LogoForm
    list_display = ['product', 'thumbnail', 'is_published']
    autocomplete_fields = ['product']

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


class StockAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Stock
    form = StockForm
    list_display = ['stock', 'product', 'warehouse']
    autocomplete_fields = ['product', 'warehouse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product', 'warehouse')
        return queryset


class ShipmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Shipment
    form = ShipmentForm
    list_display = ['stock', 'product', 'warehouse', 'date']
    autocomplete_fields = ['product', 'warehouse']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product', 'warehouse')
        return queryset


class HeroAdmin(SortableAdminMixin, BaseAdmin):
    model = Hero
    form = HeroForm
    list_display = ['name', 'is_published']

    inlines = [
        HeroItemInline,
    ]

class OfferProductInline(SortableInlineAdminMixin, admin.TabularInline):
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
