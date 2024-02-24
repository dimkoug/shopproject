from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from shop.models import (
    Category, ChildCategory, 
    Feature, FeatureCategory,
    Attribute, Product,
    ProductTag, ProductRelated,
    Media, Logo,ProductLogo, Shipment, ProductAttribute,
    Hero, HeroItem,
    Offer, OfferProduct, ShoppingCart,
    Address, Order, OrderItem,
)

from stocks.models import Stock


from .forms import (
    CategoryForm, ChildCategoryForm, ChildCategoryFormSet,
    FeatureForm, CategoryFormSet, AttributeForm,
    MediaFormSet, ProductLogoFormSet, StockFormSet,
    ProductForm, ProductTagFormSet,
    ProductRelatedFormSet, MediaForm, LogoForm,ProductLogoForm, StockForm, ShipmentForm,
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






class CategoryInline(admin.TabularInline):
    model = FeatureCategory
    formset = CategoryFormSet
    fk_name = 'feature'
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


class ProductLogoInline(admin.TabularInline):
    model = ProductLogo
    formset = ProductLogoFormSet
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




class CategoryAdmin(admin.ModelAdmin):
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



class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    form = FeatureForm
    search_fields = ['name']

    inlines = [
        CategoryInline,
    ]


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm
    list_display = ('name', 'is_published', 'feature')
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('feature')
        return queryset



class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm
    search_fields = ['name']

    inlines = [
        ProductTagInline,
        ProductRelatedInline,
        ProductAttributeInline,
        MediaInline,
        ProductLogoInline,
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


class ShipmentAdmin(admin.ModelAdmin):
    model = Shipment
    form = ShipmentForm


class HeroAdmin(admin.ModelAdmin):
    model = Hero
    form = HeroForm

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


admin.site.register(Feature, FeatureAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Logo, LogoAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Hero, HeroAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
