from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Prefetch
from django.urls import reverse_lazy

from core.views import (
    CoreListView, CoreDetailView, CoreCreateView,
    CoreUpdateView, CoreDeleteView
)

from .models import (
    Category, Supplier, Brand, BrandSupplier, Specification, Attribute, Tag,
    Product, ProductShipment, ProductMedia, ProductTag, ProductCategory,
    ProductAttribute, Hero, HeroItem
)
from .forms import (
    CategoryForm, SupplierForm, BrandForm, BrandSupplierForm,
    SpecificationForm, AttributeForm, TagForm,
    ProductForm, ProductShipmentForm, ProductMediaForm, ProductTagForm,
    ProductCategoryForm, ProductAttributeForm, HeroForm, HeroItemForm
)


class CategoryListView(CoreListView):
    model = Category
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(CoreDetailView):
    model = Category
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(CoreCreateView):
    template = 'form'
    model = Category
    form_class = CategoryForm


class CategoryUpdateView(CoreUpdateView):
    template = 'form'
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Category


class ProductListView(CoreListView):
    model = Product
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(CoreDetailView):
    model = Product
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(CoreCreateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)


class ProductUpdateView(CoreUpdateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)


class ProductDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Product


class SupplierListView(CoreListView):
    template = 'list'
    model = Supplier
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupplierDetailView(CoreDetailView):
    model = Supplier
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupplierCreateView(CoreCreateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm


class SupplierUpdateView(CoreUpdateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Supplier


class BrandListView(CoreListView):
    template = 'list'
    model = Brand
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandDetailView(CoreDetailView):
    model = Brand
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandCreateView(CoreCreateView):
    template = 'form'
    model = Brand
    form_class = BrandForm


class BrandUpdateView(CoreUpdateView):
    template = 'form'
    model = Brand
    form_class = BrandForm


class BrandDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Brand


class SpecificationListView(CoreListView):
    template = 'list'
    model = Specification
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationDetailView(CoreDetailView):
    model = Specification
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationCreateView(CoreCreateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm


class SpecificationUpdateView(CoreUpdateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm


class SpecificationDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Specification


class AttributeListView(CoreListView):
    template = 'list'
    model = Attribute
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeDetailView(CoreDetailView):
    model = Attribute
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeCreateView(CoreCreateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm


class AttributeUpdateView(CoreUpdateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm


class AttributeDeleteView(CoreDeleteView):
    template = 'confirm_delete'
    model = Attribute


class TagListView(CoreListView):
    template = 'list'
    model = Tag
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagDetailView(CoreDetailView):
    model = Tag
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagCreateView(CoreCreateView):
    template = 'form'
    model = Tag
    form_class = TagForm


class TagUpdateView(CoreUpdateView):
    template = 'form'
    model = Tag
    form_class = TagForm


class TagDeleteView(CoreDeleteView):
    template = "confirm_delete"
    model = Tag


class HeroListView(CoreListView):
    template = 'list'
    model = Hero
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeroDetailView(CoreDetailView):
    model = Hero
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeroCreateView(CoreCreateView):
    template = 'form'
    model = Hero
    form_class = HeroForm


class HeroUpdateView(CoreUpdateView):
    template = 'form'
    model = Hero
    form_class = HeroForm


class HeroDeleteView(CoreDeleteView):
    template = "confirm_delete"
    model = Hero


class HeroItemListView(CoreListView):
    template = 'list'
    model = HeroItem
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeroItemDetailView(CoreDetailView):
    model = HeroItem
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HeroItemCreateView(CoreCreateView):
    template = 'form'
    model = HeroItem
    form_class = HeroItemForm


class HeroItemUpdateView(CoreUpdateView):
    template = 'form'
    model = HeroItem
    form_class = HeroItemForm


class HeroItemDeleteView(CoreDeleteView):
    template = "confirm_delete"
    model = HeroItem
