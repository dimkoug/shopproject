from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.urls import reverse_lazy

from core.mixins import ProtectedViewMixin, ModelMixin
from .mixins import SuccessUrlMixin, MessageMixin, DynamicTemplateMixin


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


class ManageView(ProtectedViewMixin, TemplateView):
    template_name = "cms/manage.html"



class CategoryListView(ProtectedViewMixin, DynamicTemplateMixin,
                       ModelMixin, ListView):
    model = Category
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                         ModelMixin, DetailView):
    model = Category
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         MessageMixin, CreateView):
    template = 'form'
    model = Category
    form_class = CategoryForm



class CategoryUpdateView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         MessageMixin, UpdateView):
    template = 'form'
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         DeleteView):
    template = 'delete'
    model = Category



class ProductListView(ProtectedViewMixin, DynamicTemplateMixin,
                      ModelMixin, ListView):
    model = Product
    template = 'list'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                        ModelMixin, DetailView):
    model = Product
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreateView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         MessageMixin, CreateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)



class ProductUpdateView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         MessageMixin, UpdateView):
    template = 'form'
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        obj = form.save()
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                ProductMedia.objects.create(image=f, product=obj)
        return super().form_valid(form)


class ProductDeleteView(ProtectedViewMixin, ModelMixin,
                         DynamicTemplateMixin, SuccessUrlMixin,
                         DeleteView):
    template = 'delete'
    model = Product


class SupplierListView(ProtectedViewMixin, DynamicTemplateMixin,
                       ModelMixin, ListView):
    template = 'list'
    model = Supplier
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SupplierDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                         ModelMixin, DetailView):
    model = Supplier
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupplierCreateView(ProtectedViewMixin, DynamicTemplateMixin,
                         ModelMixin, SuccessUrlMixin,
                         MessageMixin, CreateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm



class SupplierUpdateView(ProtectedViewMixin, DynamicTemplateMixin,
                         ModelMixin, SuccessUrlMixin,
                         MessageMixin, UpdateView):
    template = 'form'
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(ProtectedViewMixin, DynamicTemplateMixin,
                         ModelMixin, SuccessUrlMixin,
                         DeleteView):
    template = 'delete'
    model = Supplier


class BrandListView(ProtectedViewMixin, DynamicTemplateMixin,
                    ModelMixin, ListView):
    template = 'list'
    model = Brand
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                      ModelMixin, DetailView):
    model = Brand
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandCreateView(ProtectedViewMixin, DynamicTemplateMixin,
                      ModelMixin, SuccessUrlMixin,
                      MessageMixin, CreateView):
    template = 'form'
    model = Brand
    form_class = BrandForm



class BrandUpdateView(ProtectedViewMixin, DynamicTemplateMixin,
                      ModelMixin, SuccessUrlMixin,
                      MessageMixin, UpdateView):
    template = 'form'
    model = Brand
    form_class = BrandForm


class BrandDeleteView(ProtectedViewMixin, DynamicTemplateMixin,
                      ModelMixin, SuccessUrlMixin,
                      DeleteView):
    template = 'form'
    model = Brand

class SpecificationListView(ProtectedViewMixin,DynamicTemplateMixin,
                            ModelMixin, ListView):
    template = 'list'
    model = Specification
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                              ModelMixin, DetailView):
    model = Specification
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SpecificationCreateView(ProtectedViewMixin, DynamicTemplateMixin,
                              ModelMixin, SuccessUrlMixin,
                              MessageMixin, CreateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm



class SpecificationUpdateView(ProtectedViewMixin, DynamicTemplateMixin,
                              ModelMixin, SuccessUrlMixin,
                              MessageMixin, UpdateView):
    template = 'form'
    model = Specification
    form_class = SpecificationForm


class SpecificationDeleteView(ProtectedViewMixin, DynamicTemplateMixin,
                              ModelMixin, SuccessUrlMixin,
                              DeleteView):
    template = 'delete'
    model = Specification


class AttributeListView(ProtectedViewMixin, DynamicTemplateMixin,
                        ModelMixin, ListView):
    template = 'list'
    model = Attribute
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeDetailView(ProtectedViewMixin, DynamicTemplateMixin,
                          ModelMixin, DetailView):
    model = Attribute
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeCreateView(ProtectedViewMixin, DynamicTemplateMixin,
                          ModelMixin, SuccessUrlMixin,
                          MessageMixin, CreateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm



class AttributeUpdateView(ProtectedViewMixin, DynamicTemplateMixin,
                          ModelMixin, SuccessUrlMixin,
                          MessageMixin, UpdateView):
    template = 'form'
    model = Attribute
    form_class = AttributeForm


class AttributeDeleteView(ProtectedViewMixin, DynamicTemplateMixin,
                          ModelMixin, SuccessUrlMixin,
                          DeleteView):
    template = 'delete'
    model = Attribute


class TagListView(ProtectedViewMixin, DynamicTemplateMixin,
                  ModelMixin, ListView):
    template = 'list'
    model = Tag
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagDetailView(ProtectedViewMixin,DynamicTemplateMixin,
                    ModelMixin, DetailView):
    model = Tag
    template = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TagCreateView(ProtectedViewMixin, ModelMixin,
                    DynamicTemplateMixin, SuccessUrlMixin,
                    MessageMixin, CreateView):
    template = 'form'
    model = Tag
    form_class = TagForm



class TagUpdateView(ProtectedViewMixin, DynamicTemplateMixin,
                    ModelMixin, SuccessUrlMixin,
                    MessageMixin, UpdateView):
    template = 'form'
    model = Tag
    form_class = TagForm


class TagDeleteView(ProtectedViewMixin, DynamicTemplateMixin,
                    ModelMixin, SuccessUrlMixin,  DeleteView):
    template = "delete"
    model = Tag
