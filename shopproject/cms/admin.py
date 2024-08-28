from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from shop.models import (
    Category, ChildCategory, 
    Feature, FeatureCategory,
    Attribute, Product,
    ProductTag, ProductRelated,
    ProductMedia, ProductLogo, ProductAttribute,
)

from stocks.models import Stock


from .forms import (
    CategoryForm,
    FeatureForm, CategoryFormSet, AttributeForm,
    ProductMediaFormSet, ProductLogoFormSet, StockFormSet,
    ProductForm, ProductTagFormSet,
    ProductRelatedFormSet, ProductMediaForm, ProductLogoForm, StockForm,
    ProductAttributeFormSet,
)



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


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    formset = ProductMediaFormSet
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











class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    list_display = ('name', 'thumbnail', 'is_published', 'get_categories')
    search_fields = ['name']

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
        ProductMediaInline,
        ProductLogoInline,
        StockInline
    ]


# class MediaAdmin(admin.ModelAdmin):
#     model = Media
#     form = MediaForm





class StockAdmin(admin.ModelAdmin):
    model = Stock
    form = StockForm













admin.site.register(Category, CategoryAdmin)


admin.site.register(Feature, FeatureAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Media, MediaAdmin)






