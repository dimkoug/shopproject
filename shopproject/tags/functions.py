from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from core.functions import is_ajax

from tags.models import Tag


def get_tags_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    search = request.GET.get('search')
    if search and search != '':
        data = Tag.objects.filter(
            Q(name__icontains=search)
        ).values('id', 'name')
        for d in data:
            results.append({'id':d['id'], "text": d['name']})
        # j_data = serializers.serialize("json", data, fields=('erp_code', 'title'))
        # return JsonResponse(j_data, safe=False)
    return JsonResponse({"results": results}, safe=False)