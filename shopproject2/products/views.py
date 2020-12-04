from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib import messages
from core.mixins import ProtectedViewMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import (Category, Tag, Specification, Attribute, Product, ProductTag,
                     ProductAttribute, ShoppingCartItem, Order, OrderDetail)
from .forms import (CategoryForm,TagForm,SpecificationForm,AttributeForm,ProductForm,
                    ProductTagForm, ProductAttributeForm, OrderForm)


class OrderListView(ProtectedViewMixin, ListView):

    model = Order
    paginate_by = 100  # if pagination is desired
    template_name = "my_orders.html"

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


class CategoryDetailView(DetailView):

    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        attrs = self.request.GET.getlist('attrs')
        print(attrs)
        products = Product.objects.select_related('category').filter(category=self.get_object())
        if attrs:
            products = products.filter(attributes__in=attrs)
        context['attrs_checked'] = attrs
        context['product_list'] = products
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
        context['product_list'] = Product.objects.select_related('category').filter(tags=self.get_object())
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def order(request):
    context = {}
    order_form = OrderForm(request.POST or None)
    sum = 0
    cart_id = request.session.get('cart_id')
    shopping_items = ShoppingCartItem.objects.select_related(
        'product').filter(cartId=cart_id)
    context['items'] = shopping_items
    for item in shopping_items:
        sum += item.get_price()
    template = 'order.html'
    context['sum'] = sum
    order_form.fields['amount'].initial = sum
    order_form.fields['profile'].initial = request.user.profile
    context['order_form'] = order_form
    if request.method == 'POST':
        if order_form.is_valid():
            obj = order_form.save()
            for item in shopping_items:
                detail = OrderDetail()
                detail.order = obj
                detail.product = item.product
                detail.quantity = item.quantity
                detail.save()
            ShoppingCartItem.objects.filter(cartId=cart_id).delete()
            messages.success(request, 'The order is placed successfully!')
            return redirect('home')
    return render(request, template, context)


def basket(request):
    context = {}
    sum = 0
    cart_id = request.session.get('cart_id')
    shopping_items = ShoppingCartItem.objects.select_related(
        'product').filter(cartId=cart_id)
    context['items'] = shopping_items
    for item in shopping_items:
        sum += item.get_price()
    template = 'basket.html'
    context['sum'] = sum
    return render(request, template, context)


def add_to_basket(request, id):
    cart_id = request.session.get('cart_id')
    try:
        shopping_items = ShoppingCartItem.objects.get(
            cartId=cart_id, product_id=id)
        shopping_items.quantity += 1
        shopping_items.save()
    except ShoppingCartItem.DoesNotExist:
        shopping_items = ShoppingCartItem()
        shopping_items.cartId = cart_id
        shopping_items.product_id = id
        shopping_items.save()
    messages.success(request, 'Your basket was updated successfully!')
    return redirect('basket')


def remove_from_basket(request, id):
    cart_id = request.session.get('cart_id')
    try:
        shopping_items = ShoppingCartItem.objects.get(
            cartId=cart_id, product_id=id)
        if shopping_items.quantity == 1 or shopping_items.quantity <= 1:
            ShoppingCartItem.objects.filter(
                cartId=cart_id, product_id=id).delete()
        else:
            shopping_items.quantity -=1
            shopping_items.save()
    except ShoppingCartItem.DoesNotExist:
        pass
    messages.success(request, 'Your basket was updated successfully!')
    return redirect('basket')
