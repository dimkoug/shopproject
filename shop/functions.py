from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

from core.functions import is_ajax

from .models import ShoppingCart, Product,Category, Attribute, Brand


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
    if is_ajax(request):
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
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('shop:basket')


def clear_basket(request):
    shopping_cart_id = request.session.get('shopping_cart_id')
    ShoppingCart.objects.filter(
        shopping_cart_id=shopping_cart_id).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('index')


def remove_item_from_basket(request, id):
    shopping_cart_id = request.session.get('shopping_cart_id')
    ShoppingCart.objects.filter(
        shopping_cart_id=shopping_cart_id, product_id=id).delete()
    messages.success(request, 'Your basket was cleared successfully!')
    if is_ajax(request):
        return ajax_basket(request)
    return redirect('shop:basket')


def get_products_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    search = request.GET.get('search')
    if search and search != '':
        data = Product.objects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        ).values('id', 'name')
        for d in data:
            results.append({'id':d['id'], "text": d['name']})
        # j_data = serializers.serialize("json", data, fields=('erp_code', 'title'))
        # return JsonResponse(j_data, safe=False)
    return JsonResponse({"results": results}, safe=False)


def get_attributes_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    search = request.GET.get('search')
    if search and search != '':
        data = Attribute.objects.filter(
            Q(name__icontains=search)
        ).values('id', 'name')
        for d in data:
            results.append({'id':d['id'], "text": d['name']})
        # j_data = serializers.serialize("json", data, fields=('erp_code', 'title'))
        # return JsonResponse(j_data, safe=False)
    return JsonResponse({"results": results}, safe=False)


def get_categories_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    search = request.GET.get('search')
    if search and search != '':
        data = Category.objects.filter(
            Q(name__icontains=search)
        ).values('id', 'name')
        for d in data:
            results.append({'id':d['id'], "text": d['name']})
        # j_data = serializers.serialize("json", data, fields=('erp_code', 'title'))
        # return JsonResponse(j_data, safe=False)
    return JsonResponse({"results": results}, safe=False)


def get_brands_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    search = request.GET.get('search')
    if search and search != '':
        data = Brand.objects.filter(
            Q(name__icontains=search)
        ).values('id', 'name')
        for d in data:
            results.append({'id':d['id'], "text": d['name']})
        # j_data = serializers.serialize("json", data, fields=('erp_code', 'title'))
        # return JsonResponse(j_data, safe=False)
    return JsonResponse({"results": results}, safe=False)