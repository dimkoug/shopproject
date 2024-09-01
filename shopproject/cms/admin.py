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
    FeatureForm, AttributeForm,
    ProductForm, ProductMediaForm, ProductLogoForm,
)


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


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm
    list_display = ('value', 'is_published', 'feature')
    search_fields = ['value']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('feature')
        return queryset



class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm
    search_fields = ['name']

# class MediaAdmin(admin.ModelAdmin):
#     model = Media
#     form = MediaForm





admin.site.register(Category, CategoryAdmin)


admin.site.register(Feature, FeatureAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Media, MediaAdmin)






