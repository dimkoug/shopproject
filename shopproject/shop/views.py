import uuid
from django.urls import reverse_lazy
from django.db.models import Prefetch
from django.contrib import messages
from django.http import JsonResponse
from django import template
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView


from core.mixins import PassRequestToFormViewMixin

from .models import (ProductCategory, Specification,
                     Product, ProductTag, Order, OrderDetail,
                     ProductStatistics, ShoppingCartItem, Attribute,
                     ProductMedia, ProductAttribute)

from .forms import OrderForm


class IndexView(TemplateView):
    template_name = "site/index.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('shopping_cart_id'):
            self.request.session['shopping_cart_id'] = str(uuid.uuid4())
        print('index cart: ', self.request.session['shopping_cart_id'])
        return super().dispatch(*args, **kwargs)


class CatalogListView(ListView):

    model = Product
    paginate_by = 100  # if pagination is desired
    template_name = 'site/product_list.html'
    queryset = Product.objects.select_related('brand', 'parent').prefetch_related(
        Prefetch('categories',
                 queryset=ProductCategory.objects.select_related(
                    'product', 'category'), to_attr='productcategory_list'),
        Prefetch('tags',
                 queryset=ProductTag.objects.select_related(
                    'product', 'tag'), to_attr='producttag_list'),
        Prefetch('productattributes',
                 queryset=ProductAttribute.objects.select_related(
                    'product', 'attribute'), to_attr='productattribute_list')
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        tag = self.request.GET.get('tag')
        attrs = self.request.GET.getlist('attrs')
        if category:
            p = Prefetch('categories',
                         queryset=ProductCategory.objects.select_related(
                            'product', 'category').filter(
                                category_id=category),
                         to_attr='productcategory_list')
            queryset = Product.objects.select_related(
                'brand').prefetch_related(p).filter(categories__in=category)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if tag:
            p = Prefetch('tags',
                         queryset=ProductTag.objects.select_related(
                            'product', 'tag').filter(
                                tag_id=tag), to_attr='producttag_list')
            queryset = Product.objects.select_related(
                'brand').prefetch_related(p).filter(producttags__in=tag)
        if q and q != '':
            queryset = queryset.filter(name__icontains=q)
        if len(attrs) > 0:
            p = Prefetch('productattributes',
                         queryset=ProductAttribute.objects.select_related(
                            'product', 'attribute').filter(
                                attribute_id__in=attrs),
                         to_attr='productattribute_list')
            queryset = Product.objects.select_related(
                'brand').prefetch_related(p).filter(
                    productattributes__in=attrs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attrs_checked'] = self.request.GET.getlist('attrs')
        context['specification_list'] = Specification.objects.prefetch_related(
            Prefetch('attributes',
                     queryset=Attribute.objects.select_related('specification')
                     , to_attr='attribute_list')).all()
        return context


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('profile').prefetch_related(
            Prefetch('orderdetail_set',
                     queryset=OrderDetail.objects.select_related(
                        'product', 'order')
                     )).filter(profile=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderFormView(LoginRequiredMixin, PassRequestToFormViewMixin,
                    CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/order_form.html'
    success_url = reverse_lazy("shop:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum = 0
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        shopping_items = ShoppingCartItem.objects.select_related(
            'product').filter(cartid=shopping_cart_id)
        for item in shopping_items:
            sum += item.get_price()
        context['items'] = shopping_items
        context['sum'] = sum
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        sum = self.get_context_data()['sum']
        items = self.get_context_data()['items']
        obj.amount = sum
        obj.save()
        for item in items:
            detail = OrderDetail()
            detail.order = obj
            detail.product = item.product
            detail.quantity = item.quantity
            detail.save()
            ShoppingCartItem.objects.filter(cartid=shopping_cart_id).delete()
            messages.success(self.request, 'The order is placed successfully!')
        return super().form_valid(form)


class BasketView(TemplateView):
    template_name = 'shop/basket.html'
    ajax_partial = 'shop/partials/basket_partial.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.is_ajax():
            context['ajax'] = True
            html = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html': html})
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        sum = 0
        shopping_items = ShoppingCartItem.objects.select_related(
            'product').filter(cartid=shopping_cart_id)
        for item in shopping_items:
            sum += item.get_price()
        context['sum'] = sum
        context['items'] = shopping_items
        return context


class CatalogProductDetailView(DetailView):
    model = Product
    template_name = 'site/product_detail.html'
    queryset = Product.objects.select_related('brand', 'parent').prefetch_related(
        Prefetch('categories',
                 queryset=ProductCategory.objects.select_related(
                    'category', 'product'), to_attr='productcategory_list'),
        Prefetch('producttags',
                 queryset=ProductTag.objects.select_related(
                    'tag', 'product'), to_attr='producttag_list'),
        Prefetch('productmedia',
                 queryset=ProductMedia.objects.select_related(
                     'product'), to_attr='productmedia_list'),
        Prefetch('productattributes',
                 queryset=ProductAttribute.objects.select_related(
                     'attribute', 'product'), to_attr='productattribute_list'),
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ProductStatistics.objects.create(
            journey=str(uuid.uuid4()),
            product=self.get_object()
        )
        return context
