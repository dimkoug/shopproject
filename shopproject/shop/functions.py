from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from core.functions import is_ajax

from tags.models import Tag

from .models import  Product,Category, Attribute, ProductAttribute

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








def get_attributes(request):
    id = request.GET.get('id')
    if id:
        data = Attribute.objects.filter(feature_id=id)
        sdata = serializers.serialize("json", data)
        return JsonResponse(sdata, safe=False)
    return JsonResponse({})


def set_attribute(request):
    try:
        product_id = request.POST['product']
        attribute_id = request.POST['attribute']
        product_attribute = ProductAttribute.objects.create(product_id=product_id,attribute_id=attribute_id)
        return JsonResponse({
            'feature': product_attribute.attribute.feature.name,
            'name': product_attribute.attribute.name,
            "product_id": product_attribute.product.id,
            "attribute_id": product_attribute.attribute.id
        })
    except Exception as e:
        print(e)
        raise
        return JsonResponse({})

def delete_attribute(request):
    try:
        product_id = request.POST['product']
        attribute_id = request.POST['attribute']
        product_attribute = ProductAttribute.objects.get(product_id=product_id,attribute_id=attribute_id)
        product_attribute.delete()
    except:
        pass
    return JsonResponse({})