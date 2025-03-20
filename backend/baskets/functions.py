from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string

from core.functions import is_ajax

from baskets.models import Basket



def ajax_basket(request):
    context = {}
    template_name = 'baskets/partials/basket_partial.html'
    sum = 0
    shopping_items = Basket.objects.select_related(
            'product').filter(session_key=request.session.session_key)
    for item in shopping_items:
        sum += item.product.price * item.quantity
    context['sum'] = sum
    context['items'] = shopping_items
    context['ajax'] = True
    html = render_to_string(
            template_name, context, request)
    return JsonResponse({'html': html})


def add_to_basket(request, id):
    
    try:
        shopping_items = Basket.objects.select_related('product').get(
            session_key=request.session.session_key, product_id=id)
        shopping_items.quantity += 1
        shopping_items.save()
    except Basket.DoesNotExist:
        shopping_items = Basket()
        shopping_items.session_key = request.session.session_key
        shopping_items.product_id = id
        shopping_items.save()
    messages.success(request, 'Your basket was updated successfully!')
    if is_ajax(request):
        return ajax_basket(request)

    return redirect('baskets:basket')


def remove_from_basket(request, id):
    try:
        shopping_items = Basket.objects.select_related('product').get(
            session_key=request.session.session_key, product_id=id)
        if shopping_items.quantity == 1 or shopping_items.quantity <= 1:
            Basket.objects.select_related('product').filter(
                session_key=request.session.session_key, product_id=id).delete()
        else:
            shopping_items.quantity -= 1
            shopping_items.save()
    except Basket.DoesNotExist:
        pass
    messages.success(request, 'Your basket was updated successfully!')
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('baskets:basket')


def clear_basket(request):
    Basket.objects.filter(
        session_key=request.session.session_key).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('index')


def remove_item_from_basket(request, id):
    Basket.objects.select_related('session').filter(
        session_key=request.session.session_key, product_id=id).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('baskets:basket')