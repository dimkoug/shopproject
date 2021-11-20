import uuid
from django.urls import reverse_lazy
from django.db.models import Prefetch, Count, Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django import template
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from profiles.views import ProtectProfile


from core.mixins import (
    PassRequestToFormViewMixin, PaginationMixin, FormMixin
)
from .models import (
    ProductCategory, Feature, Product, ProductTag, Order, OrderItem,
    ShoppingCartItem, Attribute, Address,
    Media, ProductAttribute
)

from .forms import (
    SiteOrderForm, SiteAddressForm
)


class IndexView(TemplateView):
    template_name = "shop/site/index.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('shopping_cart_id'):
            self.request.session['shopping_cart_id'] = str(uuid.uuid4())
        print('index cart: ', self.request.session['shopping_cart_id'])
        return super().dispatch(*args, **kwargs)


class CatalogListView(PaginationMixin, ListView):

    model = Product
    paginate_by = 100  # if pagination is desired
    template_name = 'shop/site/product_list.html'
    ajax_partial = 'shop/partials/product_ajax_list_partial.html'

    queryset = Product.objects.select_related('brand', 'parent').prefetch_related(
        Prefetch('productcategories',
                 queryset=ProductCategory.objects.select_related(
                    'product', 'category'), to_attr='productcategory_list'),
        Prefetch('producttags',
                 queryset=ProductTag.objects.select_related(
                    'product', 'tag'), to_attr='producttag_list'),
        Prefetch('productattributes',
                 queryset=ProductAttribute.objects.select_related(
                    'product', 'attribute'), to_attr='productattribute_list')
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        attrs = []
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        tag = self.request.GET.get('tag')
        features = [feature for feature in self.request.GET.keys() if feature.startswith('feature')]
        for feature in features:
            attrs.append(self.request.GET.getlist(feature))
        if category:
            p = Prefetch(
                'productcategories',
                queryset=ProductCategory.objects.select_related(
                        'product', 'category').filter(category_id=category),
            )
            queryset = Product.objects.select_related(
                'brand').prefetch_related(p).filter(categories__in=category)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if tag:
            p = Prefetch('producttags',
                         queryset=ProductTag.objects.select_related(
                            'product', 'tag').filter(
                                tag_id=tag))
            queryset = Product.objects.select_related(
                'brand').prefetch_related(p).filter(producttags__in=tag)
        if q and q != '':
            queryset = queryset.filter(name__icontains=q)
        if len(attrs) > 0:
            for attr in attrs:
                p = Prefetch('productattributes',
                             queryset=ProductAttribute.objects.select_related(
                                'product', 'attribute').filter(
                                    attribute_id__in=attr),
                             to_attr='productattribute_list')
                queryset = Product.objects.select_related(
                    'brand').prefetch_related(p).filter(
                        productattributes__in=attr)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
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
        attrs = []
        attrs_checked = []
        features = [feature for feature in self.request.GET.keys() if feature.startswith('feature')]
        for feature in features:
            attrs.append(self.request.GET.getlist(feature))
        for arrt in attrs:
            for item in arrt:
                attrs_checked.append(item)
        context['attrs_checked'] = attrs_checked
        counter = Count('product', filter=Q(product__in=self.get_queryset()))
        context['specification_list'] = Feature.objects.prefetch_related(
            Prefetch('attributes',
                     queryset=Attribute.objects.select_related(
                        'feature').prefetch_related(
                            Prefetch('productattributes',
                                     queryset=ProductAttribute.objects.select_related(
                                        'product', 'attribute').annotate(
                                        product_counter=counter),
                                     to_attr='attr_list'))
                     , to_attr='attribute_list')).all()
        context['products_count'] = self.get_queryset().count()
        return context


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    paginate_by = 100  # if pagination is desired
    template_name = 'shop/site/order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('billing_address', 'shipping_address').prefetch_related(
            Prefetch('orderitems',
                     queryset=OrderItem.objects.select_related(
                        'product', 'order')
                     )).filter(billing_address__profile=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderFormView(LoginRequiredMixin, PassRequestToFormViewMixin,
                    FormMixin, CreateView):
    model = Order
    form_class = SiteOrderForm
    template_name = 'shop/site/order_form.html'
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum = 0
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        shopping_items = ShoppingCartItem.objects.select_related(
            'product').filter(shopping_cart_id=shopping_cart_id)
        for item in shopping_items:
            sum += item.product.price
        context['items'] = shopping_items
        context['sum'] = sum
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        sum = self.get_context_data()['sum']
        items = self.get_context_data()['items']
        obj.order_registration = str(uuid.uuid4())[-10:]
        obj.total = sum
        obj.save()
        for item in items:
            detail = OrderItem()
            detail.order = obj
            detail.product = item.product
            detail.quantity = item.quantity
            detail.save()
            ShoppingCartItem.objects.filter(shopping_cart_id=shopping_cart_id).delete()
            messages.success(self.request, 'The order is placed successfully!')
        return super().form_valid(form)


class BasketView(TemplateView):
    template_name = 'shop/site/basket.html'
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
            'product').filter(shopping_cart_id=shopping_cart_id)
        for item in shopping_items:
            sum += item.product.price * item.quantity
        context['sum'] = sum
        context['items'] = shopping_items
        return context


class CatalogProductDetailView(DetailView):
    model = Product
    template_name = 'shop/site/product_detail.html'
    queryset = Product.objects.select_related('brand', 'parent').prefetch_related(
        Prefetch('productcategories',
                 queryset=ProductCategory.objects.select_related(
                    'category', 'product'), to_attr='productcategory_list'),
        Prefetch('producttags',
                 queryset=ProductTag.objects.select_related(
                    'tag', 'product'), to_attr='producttag_list'),
        Prefetch('media',
                 queryset=Media.objects.select_related(
                     'product'), to_attr='productmedia_list'),
        Prefetch('productattributes',
                 queryset=ProductAttribute.objects.select_related(
                     'attribute', 'product'), to_attr='productattribute_list'),
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddressCreateView(FormMixin, CreateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'shop/site/address_form.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_anonymous:
            obj.profile = self.request.user.profile
        address_type = self.request.GET.get('addr')
        if address_type is not None:
            address_type = Address.ADDRESS_CHOICES[int(address_type)][0]
            obj.address_type = address_type
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(ProtectProfile, FormMixin, UpdateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'shop/site/address_form.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url


class AddressDeleteView(ProtectProfile, FormMixin, DeleteView):
    model = Address
    template_name = 'shop/site/address_form_confirm_delete.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url
