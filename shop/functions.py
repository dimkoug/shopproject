from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import ShoppingCart


def create_query_string(request):
    query_string = ''
    for key in request.GET.keys():
        if key != 'page':
            value = request.GET.getlist(key)
            if len(value) > 0:
                for item in value:
                    if value != '':
                        query_string += "&{}={}".format(key, item)
            else:
                if value != '':
                    query_string += "&{}={}".format(key, value)
    return query_string


def ajax_basket(request):
    context = {}
    template_name = 'shop/partials/basket_partial.html'
    shopping_cart_id = request.session.get('shopping_cart_id')
    sum = 0
    shopping_items = ShoppingCart.objects.select_related(
            'product').filter(shopping_cart_id=shopping_cart_id)
    for item in shopping_items:
        sum += item.product.price * item.quantity
    context['sum'] = sum
    context['items'] = shopping_items
    context['ajax'] = True
    html = render_to_string(
            template_name, context, request)
    return JsonResponse({'html': html})


def add_to_basket(request, id):
    shopping_cart_id = request.session.get('shopping_cart_id')
    print('shopping cart id:', shopping_cart_id)
    try:
        shopping_items = ShoppingCart.objects.get(
            shopping_cart_id=shopping_cart_id, product_id=id)
        shopping_items.quantity += 1
        shopping_items.save()
    except ShoppingCart.DoesNotExist:
        shopping_items = ShoppingCart()
        shopping_items.shopping_cart_id = shopping_cart_id
        shopping_items.product_id = id
        shopping_items.save()
    messages.success(request, 'Your basket was updated successfully!')
    if request.is_ajax():
        return ajax_basket(request)

    return redirect('shop:basket')


def remove_from_basket(request, id):
    shopping_cart_id = request.session.get('shopping_cart_id')
    try:
        shopping_items = ShoppingCart.objects.get(
            shopping_cart_id=shopping_cart_id, product_id=id)
        if shopping_items.quantity == 1 or shopping_items.quantity <= 1:
            ShoppingCart.objects.filter(
                shopping_cart_id=shopping_cart_id, product_id=id).delete()
        else:
            shopping_items.quantity -= 1
            shopping_items.save()
    except ShoppingCart.DoesNotExist:
        pass
    messages.success(request, 'Your basket was updated successfully!')
    if request.is_ajax():
        return ajax_basket(request)
    return redirect('shop:basket')


def clear_basket(request):
    shopping_cart_id = request.session.get('shopping_cart_id')
    ShoppingCart.objects.filter(
        shopping_cart_id=shopping_cart_id).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if request.is_ajax():
        return ajax_basket(request)
    return redirect('index')


def remove_item_from_basket(request, id):
    shopping_cart_id = request.session.get('shopping_cart_id')
    ShoppingCart.objects.filter(
        shopping_cart_id=shopping_cart_id, product_id=id).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if request.is_ajax():
        return ajax_basket(request)
    return redirect('shop:basket')