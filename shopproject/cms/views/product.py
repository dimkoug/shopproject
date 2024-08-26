from django.shortcuts import render, redirect
from django.urls import reverse
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
from cms.views.core import CmsListView

from core.functions import is_ajax


from shop.models import (
    Product, ProductTag, ProductAttribute, ProductRelated, ProductMedia, ProductLogo,Category

)

from media.models import Media 
from logos.models import Logo

from stocks.models import Stock


from cms.forms import (
    ProductForm, ProductTagFormSet,
    ProductRelatedFormSet,
    ProductAttributeFormSet,
    ProductMediaFormSet, ProductLogoFormSet, StockFormSet
)


class ProductListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Product
    paginate_by = 50
    queryset = Product.objects.select_related('brand', 'category').order_by('order')
    fields = [
        {
        'verbose_name': 'Image',
        'db_name':'image'
        },
        {
            'verbose_name': 'Order',
            'db_name': 'order'
        },
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
        {
        'verbose_name': 'Brand',
        'db_name':'brand'
        },
        {
        'verbose_name': 'Code',
        'db_name':'code'
        },
        {
        'verbose_name': 'Category',
        'db_name':'category'
        },
        {
        'verbose_name': 'Published',
        'db_name':'is_published'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        print(category)
        if category and category != '':
            queryset = queryset.filter(category=category)
        if brand and brand != '':
            queryset = queryset.filter(brand=brand)
        return queryset


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
                        'product', 'tag')),
                "sb_url": reverse("shop:get_tags_for_sb")
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                    self.request.POST or None,
                    queryset=ProductRelated.objects.select_related(
                        'source', 'target')),
                "sb_url": reverse("shop:get_products_for_sb")
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
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                for f in formset:
                    print(f.fields)
                    for field in f.fields:
                        if 'category' == field:
                            print("category queryset")
                            f['category'].queryset = Category.objects.all()
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
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('category__featurecategories', 'attributes','tags','relatedproducts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Product Tags',
                'formset': ProductTagFormSet(
                    self.request.POST or None,instance=self.get_object(),
                    queryset=ProductTag.objects.select_related(
                        'product', 'tag')),
                "sb_url": reverse("shop:get_tags_for_sb")
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                    self.request.POST or None,instance=self.get_object(),
                    queryset=ProductRelated.objects.select_related(
                        'source', 'target')),
                "sb_url": reverse("shop:get_products_for_sb")
            },
            {
                'title': 'Stock',
                'formset': StockFormSet(
                    self.request.POST or None, self.request.FILES or None,instance=self.get_object(),
                    queryset=Stock.objects.select_related(
                        'product', 'warehouse'))
            },
        ]
        features = []
        for feature in self.get_object().category.featurecategories.all():
            features.append(feature.feature)
        context['features'] = set(features)
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                for f in formset:
                    print(f.fields)
                    for field in f.fields:
                        if 'category' == field:
                            print("category queryset")
                            f['category'].queryset = Category.objects.all()
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
            logos = self.request.FILES.getlist('logos')
            if logos:
                for f in logos:
                    l = Logo()
                    l.image = f
                    l.save()
                    ProductLogo.objects.get_or_create(product=self.get_object(),logo=l)
                    print("logo saved")
            media = self.request.FILES.getlist('media')
            if media:
                for m in media:
                    l = Media()
                    l.image = m
                    l.save()
                    ProductMedia.objects.get_or_create(product=self.get_object(),media=l)
                    print("media saved")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Product
