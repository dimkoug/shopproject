from django.contrib import admin


from core.admin  import BaseAdmin


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


class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'parent', 'is_published')
    list_filter = ('parent', 'is_published')
    list_select_related = ('parent',)
    search_fields = ['name']
    model = Category
    form = CategoryForm
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("name",)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class BrandAdmin(BaseAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ['name']
    model = Brand
    form = BrandForm
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(BaseAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ['name']
    model = Tag
    form = TagForm


class SpecificationAdmin(BaseAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ['name']
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

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category':
            field.queryset = field.queryset.filter(is_published=True, parent__isnull=False, level__gt=1)
        return field


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet

class ProductMediaAdmin(admin.ModelAdmin):
    model = ProductMedia
    form = ProductMediaForm

class ProductAdmin(BaseAdmin):
    list_display = ('name', 'parent', 'brand', 'is_published')
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
        ProductCategoryInline
    ]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Product.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ProductShipment, ProductShipmentAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(ProductMedia, ProductMediaAdmin)
admin.site.register(Product, ProductAdmin)
