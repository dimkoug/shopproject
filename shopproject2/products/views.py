from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib import messages
from core.mixins import ProtectedViewMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from .models import (Brand,Category, ProductCategory,Tag, Specification, Attribute, Product, ProductTag,
                     ProductAttribute, ShoppingCartItem)
from .forms import (CategoryForm,TagForm,SpecificationForm,AttributeForm,ProductForm,
                    ProductTagForm, ProductAttributeForm)



class BrandDetailView(DetailView):

    model = Brand
    template_name = 'brand_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.select_related('brand').filter(is_published=True,brand=self.get_object())
        context['product_list'] = product_list
        return context


class CategoryDetailView(DetailView):

    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attrs = self.request.GET.getlist('attrs')
        print(attrs)
        productcategories = ProductCategory.objects.select_related('product','category').filter(category=self.get_object())
        if attrs:
            productcategories = productcategories.filter(product__attributes__in=attrs)
        context['attrs_checked'] = attrs
        context['productcategory_list'] = productcategories
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
        context['product_list'] = Product.objects.filter(tags=self.get_object())
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
