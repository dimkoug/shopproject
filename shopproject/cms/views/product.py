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

from cms.cms_views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.functions import is_ajax


from shop.models import (
    Product, ProductTag, ProductRelated, ProductMedia, ProductLogo,Category

)

from media.models import Media 
from logos.models import Logo

from stocks.models import Stock


from cms.forms import ProductForm


class ProductListView(BaseListView):
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


class ProductDetailView(BaseDetailView):
    model = Product


class ProductCreateView(BaseCreateView):
    model = Product
    form_class = ProductForm



class ProductUpdateView(BaseUpdateView):
    model = Product
    form_class = ProductForm
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('category__featurecategories', 'attributes','tags','relatedproducts')


    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
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


class ProductDeleteView(BaseDeleteView):
    model = Product
