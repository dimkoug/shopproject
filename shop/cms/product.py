from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from core.views import (
    BaseIndexView, BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.mixins import FormMixin, SuccessUrlMixin

from core.functions import is_ajax


from shop.models import (
    Product, ProductTag, ProductAttribute, ProductCategory, ProductRelated, Media, Logo, Stock

)


from shop.forms import (
    ProductForm, ProductTagFormSet,
    ProductRelatedFormSet,
    ProductAttributeFormSet,
    MediaFormSet, LogoFormSet, StockFormSet, ProductCategoryFormSet
)


class ProductListView(LoginRequiredMixin, BaseListView):
    model = Product
    paginate_by = 50


class ProductDetailView(LoginRequiredMixin, BaseDetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseCreateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Product Tags',
                'formset': ProductTagFormSet(
                    self.request.POST or None,
                    queryset=ProductTag.objects.select_related(
                        'product', 'tag'))
            },
            {
                'title': 'Product Attributes',
                'formset': ProductAttributeFormSet(
                    self.request.POST or None,
                    queryset=ProductAttribute.objects.select_related(
                        'product', 'attribute'))
            },
            {
                'title': 'Product Categories',
                'formset': ProductCategoryFormSet(
                    self.request.POST or None,
                    queryset=ProductCategory.objects.select_related(
                        'product', 'category'))
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                    self.request.POST or None,
                    queryset=ProductRelated.objects.select_related(
                        'source', 'target'))
            },
            {
                'title': 'Media',
                'formset': MediaFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    queryset=Media.objects.select_related('product'))
            },
            {
                'title': 'Logo',
                'formset': LogoFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    queryset=Logo.objects.select_related('product'))
            },
            {
                'title': 'Stock',
                'formset': StockFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    queryset=Stock.objects.select_related(
                        'product', 'warehouse'))
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ProductAttributeFormSet(self.request.POST, instance=obj),
                ProductCategoryFormSet(self.request.POST, instance=obj),
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                MediaFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
                LogoFormSet(self.request.POST, self.request.FILES,
                            instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseUpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Product Tags',
                'formset': ProductTagFormSet(
                    self.request.POST or None, instance=self.get_object(),
                    queryset=ProductTag.objects.select_related(
                        'product', 'tag'))
            },
            {
                'title': 'Product Attributes',
                'formset': ProductAttributeFormSet(
                    self.request.POST or None, instance=self.get_object(),
                    queryset=ProductAttribute.objects.select_related(
                        'product', 'attribute'))
            },
            {
                'title': 'Product Categories',
                'formset': ProductCategoryFormSet(
                    self.request.POST or None, instance=self.get_object(),
                    queryset=ProductCategory.objects.select_related(
                        'product', 'category'))
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                    self.request.POST or None, instance=self.get_object(),
                    queryset=ProductRelated.objects.select_related(
                        'source', 'target'))
            },
            {
                'title': 'Media',
                'formset': MediaFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    instance=self.get_object(),
                    queryset=Media.objects.select_related('product'))
            },
            {
                'title': 'Logo',
                'formset': LogoFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    instance=self.get_object(),
                    queryset=Logo.objects.select_related('product'))
            },
            {
                'title': 'Stock',
                'formset': StockFormSet(
                    self.request.POST or None, self.request.FILES or None,
                    instance=self.get_object(),
                    queryset=Stock.objects.select_related(
                        'product', 'warehouse'))
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ProductAttributeFormSet(self.request.POST, instance=obj),
                ProductCategoryFormSet(self.request.POST, instance=obj),
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                MediaFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
                LogoFormSet(self.request.POST, self.request.FILES,
                            instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Product
