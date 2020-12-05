from django.contrib import admin

from .models import (Category,Tag,Specification,Attribute,Product,ProductTag,
                     ProductAttribute,ProductCategory,
                     Brand,ProductMedia,
                     ProductShipment)
from .forms import (CategoryForm,TagForm,BrandForm,
                    SpecificationForm,AttributeForm,
                    ProductShipmentForm,
                    ProductForm,ProductTagForm, ProductAttributeForm,
                    ProductTagFormSet,ProductCategoryFormSet,
                    ProductAttributeFormSet, ProductMediaForm)


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm


class SpecificationAdmin(admin.ModelAdmin):
    model = Specification
    form = SpecificationForm


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm


class ProductShipmentAdmin(admin.ModelAdmin):
    model = ProductShipment
    form = ProductShipmentForm


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    formset = ProductCategoryFormSet

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet

class ProductMediaAdmin(admin.ModelAdmin):
    model = ProductMedia
    form = ProductMediaForm

class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductAttributeInline,
        ProductTagInline,
        ProductCategoryInline
    ]


admin.site.register(ProductShipment, ProductShipmentAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(ProductMedia, ProductMediaAdmin)
admin.site.register(Product, ProductAdmin)
