from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.template.loader import render_to_string

from core.functions import is_ajax, get_sb_data

from suppliers.models import Supplier


def get_suppliers_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Supplier
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        data = model.objects.filter(q_objects)
    else:
        data = model.objects.all()
    
    
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)

    




