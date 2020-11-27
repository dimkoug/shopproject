from django.contrib import admin

from .models import (Category,Tag,Feature,Attribute,Product,ProductTag,
                     ProductAttribute, Order, OrderDetail,Brand)
from .forms import (CategoryForm,TagForm,BrandForm,FeatureForm,AttributeForm,
                    ProductForm,ProductTagForm, ProductAttributeForm,
                    ProductTagFormSet, ProductAttributeFormSet)


class OrderAdmin(admin.ModelAdmin):
    model = Order


class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm


class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm


class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    form = FeatureForm


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm

class ProductTagInline(admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet


class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductAttributeInline,
        ProductTagInline,
    ]


admin.site.register(Brand, BrandAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
