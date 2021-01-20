from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.urls import reverse_lazy

from .mixins import BaseViewMixin, FormViewMixin


from products.models import (
    Category, Supplier, Brand, BrandSupplier, Specification, Attribute, Tag,
    Product, ProductShipment, ProductMedia, ProductTag, ProductCategory,
    ProductAttribute
)
from products.forms import (
    CategoryForm, SupplierForm, BrandForm, BrandSupplierForm,
    SpecificationForm, AttributeForm, TagForm,
    ProductForm, ProductShipmentForm, ProductMediaForm, ProductTagForm,
    ProductCategoryForm,
    ProductAttributeForm
)


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = "cms/manage.html"


class CategoryListView(BaseViewMixin, ListView):
    model = Category
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(BaseViewMixin, DetailView):
    model = Category
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Category
    form_class = CategoryForm



class CategoryUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(FormViewMixin, DeleteView):
    template = 'confirm_delete'
    model = Category



class ProductListView(BaseViewMixin, ListView):
    model = Product
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(BaseViewMixin, DetailView):
    model = Product
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)



class ProductUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)


class ProductDeleteView(FormViewMixin,DeleteView):
    template = 'confirm_delete'
    model = Product


class SupplierListView(BaseViewMixin, ListView):
    template = 'list'
    model = Supplier
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SupplierDetailView(BaseViewMixin, DetailView):
    model = Supplier
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupplierCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm



class SupplierUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(FormViewMixin, DeleteView):
    template = 'confirm_delete'
    model = Supplier


class BrandListView(BaseViewMixin, ListView):
    template = 'list'
    model = Brand
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandDetailView(BaseViewMixin, DetailView):
    model = Brand
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Brand
    form_class = BrandForm



class BrandUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Brand
    form_class = BrandForm


class BrandDeleteView(FormViewMixin, DeleteView):
    template = 'confirm_delete'
    model = Brand

class SpecificationListView(BaseViewMixin, ListView):
    template = 'list'
    model = Specification
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationDetailView(BaseViewMixin, DetailView):
    model = Specification
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm



class SpecificationUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm


class SpecificationDeleteView(FormViewMixin, DeleteView):
    template = 'confirm_delete'
    model = Specification


class AttributeListView(BaseViewMixin, ListView):
    template = 'list'
    model = Attribute
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeDetailView(BaseViewMixin, DetailView):
    model = Attribute
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm



class AttributeUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm


class AttributeDeleteView(FormViewMixin, DeleteView):
    template = 'confirm_delete'
    model = Attribute


class TagListView(BaseViewMixin, ListView):
    template = 'list'
    model = Tag
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagDetailView(BaseViewMixin, DetailView):
    model = Tag
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagCreateView(FormViewMixin, CreateView):
    template = 'form'
    model = Tag
    form_class = TagForm



class TagUpdateView(FormViewMixin, UpdateView):
    template = 'form'
    model = Tag
    form_class = TagForm


class TagDeleteView(FormViewMixin,  DeleteView):
    template = "confirm_delete"
    model = Tag
