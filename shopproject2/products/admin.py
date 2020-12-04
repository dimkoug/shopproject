from django.contrib import admin

from .models import (Category,Tag,Specification,Attribute,Product,ProductTag,
                     ProductAttribute,ProductCategory, Order, OrderDetail,
                     Brand,Offer,OfferDetail)
from .forms import (CategoryForm,TagForm,BrandForm,
                    SpecificationForm,AttributeForm,
                    ProductForm,ProductTagForm, ProductAttributeForm,
                    ProductTagFormSet,ProductCategoryFormSet,
                    ProductAttributeFormSet,OfferForm,
                    OfferDetailForm)


class OrderAdmin(admin.ModelAdmin):
    model = Order


class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    form = CategoryForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm


class OfferDetailAdmin(admin.ModelAdmin):
    model = OfferDetail
    form = OfferDetailForm


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    form = BrandForm


class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm


class SpecificationAdmin(admin.ModelAdmin):
    model = Specification
    form = SpecificationForm


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    form = AttributeForm

class ProductTagInline(admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet

class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    formset = ProductCategoryFormSet

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
        ProductCategoryInline
    ]


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
