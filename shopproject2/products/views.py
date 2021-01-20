from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from core.functions import id_generator
from core.pagination import get_pagination

from .models import (Brand,Category, ProductCategory,Tag, Specification,
                     Attribute, Product, ProductTag,
                     ProductAttribute,ProductStatistics, ShoppingCartItem)
from .forms import (CategoryForm,TagForm,SpecificationForm,AttributeForm,
                    ProductForm,
                    ProductTagForm, ProductAttributeForm)



class BrandDetailView(DetailView):

    model = Brand
    template_name = 'brand_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.select_related('brand').filter(
            is_published=True,brand=self.get_object())
        context['product_list'] = get_pagination(self.request,product_list,
            settings.PRODUCT_LIST_ITEMS)
        return context


class CategoryDetailView(DetailView):

    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attrs = self.request.GET.getlist('attrs')
        print(attrs)
        productcategories = ProductCategory.objects.select_related(
            'product','category').filter(category=self.get_object())
        if attrs:
            productcategories = productcategories.filter(
                product__attributes__in=attrs)
        context['attrs_checked'] = attrs
        context['productcategory_list'] = get_pagination(self.request,productcategories,
            settings.PRODUCT_LIST_ITEMS)
        context['specification_list'] = Specification.objects.select_related(
            'category').prefetch_related(
                Prefetch('attributes',
                    queryset=Attribute.objects.select_related('specification__category')
                )).filter(category=self.get_object())
        return context


class TagDetailView(DetailView):

    model = Tag
    template_name = 'tag_detail.html'
    slug_url_kwarg = 'name'
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.filter(tags=self.get_object())
        context['product_list'] = get_pagination(self.request,product_list,
            settings.PRODUCT_LIST_ITEMS)
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = 'product_detail.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('id'):
             self.request.session['id'] = id_generator(256)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(self.request.session.get('id')):
            ProductStatistics.create(journey=self.request.session.get('id'),
            product=self.get_object())
        return context
