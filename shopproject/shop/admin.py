from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin
from core.admin  import BaseAdmin, ImageAdminMixin

from core.forms import AdminImageWidget

from .models import (Category,Tag,Specification,Attribute,Product,ProductTag,
                     ProductAttribute,ProductCategory,
                     Brand,ProductMedia,
                     Supplier,BrandSupplier,
                     ProductShipment)
from .forms import (CategoryForm,TagForm,BrandForm,
                    SpecificationForm,AttributeForm,
                    ProductShipmentForm,
                    SupplierForm, BrandSupplierFormSet,
                    ProductForm,ProductTagForm, ProductAttributeForm,
                    ProductTagFormSet,ProductCategoryFormSet,
                    ProductAttributeFormSet,ProductMediaFormSet, ProductMediaForm)

from .models import Order, OrderDetail, OrderStatus
from .forms import OrderForm, OrderDetailForm


from .models import Offer,OfferDetail
from .forms import OfferForm, OfferDetailForm

class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm


class OfferDetailAdmin(admin.ModelAdmin):
    model = OfferDetail
    form = OfferDetailForm


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)


class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = OrderForm

class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail
    form = OrderDetailForm

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(OrderStatus, admin.ModelAdmin)



class CategoryAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ['name', 'parent', 'is_published'] + BaseAdmin.list_display
    list_filter = ('parent', 'is_published')
    list_select_related = ('parent',)
    search_fields = ['name']
    model = Category
    form = CategoryForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            pk = request.resolver_match.kwargs.get("object_id")
            if(pk):
                kwargs["queryset"] = Category.objects.exclude(
                    pk=pk)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)



class BrandSupplierInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BrandSupplier
    formset = BrandSupplierFormSet


class BrandAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ['name', 'is_published'] + BaseAdmin.list_display
    list_filter = ('is_published',)
    search_fields = ['name']
    model = Brand
    form = BrandForm
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        BrandSupplierInline,
    ]


class TagAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ['name']
    model = Tag
    form = TagForm

class SupplierAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ('name', )
    search_fields = ['name']
    model = Supplier
    form = SupplierForm


class SpecificationAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ['name']
    model = Specification
    form = SpecificationForm


class AttributeAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = Attribute
    form = AttributeForm


class ProductShipmentAdmin(admin.ModelAdmin):
    model = ProductShipment
    form = ProductShipmentForm


class ProductTagInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductTag
    formset = ProductTagFormSet

class ProductCategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductCategory
    formset = ProductCategoryFormSet

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category':
            field.queryset = field.queryset.filter(is_published=True, parent__isnull=False, level__gt=1)
        return field


class ProductAttributeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet

class ProductMediaInline(SortableInlineAdminMixin, ImageAdminMixin, admin.TabularInline):
    model = ProductMedia
    formset = ProductMediaFormSet

class ProductMediaAdmin(ImageAdminMixin, admin.ModelAdmin):
    model = ProductMedia
    form = ProductMediaForm


class ProductAdmin(SortableAdminMixin, BaseAdmin):
    list_display = ['name', 'parent', 'brand', 'is_published'] + BaseAdmin.list_display
    list_filter = ('parent','brand', 'is_published')
    list_select_related = ('parent', 'brand')
    search_fields = ['name', 'brand']
    model = Product
    form = ProductForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductAttributeInline,
        ProductTagInline,
        ProductCategoryInline,
        ProductMediaInline
    ]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            pk = request.resolver_match.kwargs.get("object_id")
            if(pk):
                kwargs["queryset"] = Product.objects.exclude(
                    pk=pk)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(ProductShipment, ProductShipmentAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(ProductMedia, ProductMediaAdmin)
admin.site.register(Product, ProductAdmin)
