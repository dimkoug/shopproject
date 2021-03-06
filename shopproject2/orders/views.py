from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from products.models import ShoppingCartItem
from .models import Order, OrderDetail

from .forms import OrderForm


class OrderListView(LoginRequiredMixin, ListView):

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
