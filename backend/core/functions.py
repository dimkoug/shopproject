import random
import string
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.utils.safestring import mark_safe
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile, FileField
from decimal import Decimal
from django.utils.html import format_html


def unique_items(keys, objects):
    # Extract relevant items based on keys, filter out null/empty string values, and create frozensets for uniqueness
    items = [
        {key: obj[key] for key in keys if key in obj and obj[key] is not None and obj[key] != ""}
        for obj in objects
    ]
    # Use frozenset to ensure uniqueness
    set_of_dicts = {frozenset(d.items()) for d in items}
    # Convert back to dictionaries for easier usability
    unique_dicts = [dict(s) for s in set_of_dicts]
    print(len(unique_dicts))
    return unique_dicts



def get_pagination(request, queryset, items):
    '''
    items: The number for pagination

    return tuple (paginator, total_pages, paginated queryset) 
    '''
    paginator = Paginator(queryset, items)
    page = request.GET.get('page')
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    return (paginator, paginator.num_pages, items_page)


def is_ajax(request):
    # Check if it's an AJAX request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        origin = request.headers.get("Origin") or request.headers.get("Referer")

        if origin:
            allowed_origins = getattr(settings, "ALLOWED_ORIGINS", [])
            
            if any(origin.startswith(allowed) for allowed in allowed_origins):
                return True

    return False


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


def get_sb_data(request, model):
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


def get_select_2_data(request):
    model_str = request.GET.get('model')
    app_str = request.GET.get('app')
    q_objects = Q()
    d_objects = []
    q = request.GET.get('search')
    model = apps.get_model(app_label=app_str, model_name=model_str)
    for f in  model._meta.get_fields():
        if f.__class__.__name__  in ['CharField', 'TextField']:
            str_q = f"Q({f.name}__icontains=str('{q}'))"
            q_obj = eval(str_q)
            q_objects |= q_obj
    data = model.objects.filter(q_objects)
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results":d_objects},safe=False)

def get_rows(fields, object_list):
    '''
    fields : [{'verbose_name': 'Name', 'db_name': 'name'}]
    object_list : queryset
    '''
    db_fields = set([d['db_name'] for d in fields])
    if 'order' in db_fields:
        order = True
    else:
        order = False
    table = "<table class='table table-striped'>"
    thead = '<thead><tr>'
    for field in fields:
        thead += f"<th>{field['verbose_name']}</th>"
    thead += '</tr></thead>'
    if order:
        table += thead + '<tbody class="order">'
    else:
        table += thead + '<tbody>'
    for obj in object_list:
        model_name = obj.__class__.__name__.lower()
        if order:
            tr = f"<tr class='item' data-pk={obj.pk} data-model={model_name}>"
        else:
            tr = '<tr>'
        print(obj._meta.fields)
        app = obj._meta.app_label
        model = obj.__class__.__name__.lower()
        update_url = reverse_lazy(f"{app}:{model}-update",kwargs={"pk":obj.pk})
        delete_url = reverse_lazy(f"{app}:{model}-delete",kwargs={"pk":obj.pk})
        for field in fields:
            db_name = field['db_name']
            if db_name == 'order':
                value = '<i class="bi bi-list"></i>'
            else:
                value = getattr(obj, db_name)
                if isinstance(value, Decimal):
                    value = round(value,0)
                elif isinstance(value, bool):
                    if value:
                        value = format_html(mark_safe('<i class="bi bi-check-lg text-success"></i>'))
                    else:
                        value = format_html(mark_safe('<i class="bi bi-x-lg text-danger"></i>'))
                elif isinstance(value, models.Manager):
                    print(f"{value} is a related manager.")
                    related_objects = value.get_queryset()
                    value = '<ul>'
                    for obj in related_objects:
                        value += f'<li>{obj}</li>'
                    value += '</ul>'
                elif isinstance(value,ImageFieldFile):
                    if value and value.url:
                        value = format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
            tr += '<td>' + str(value) + '</td>'
        tr += f"""<td><a href='{update_url}'>{format_html(mark_safe('<i class="bi bi-pencil-square text-warning" style="font-size:1.5rem;"></i>'))}</a><a href='{delete_url}        'class='delete-tr'>{format_html(mark_safe('<i class="bi bi-x text-danger" style="font-size:1.5rem;"></i>'))}</a></td>"""
        
        tr += '</tr>'
        table += tr
    table += '</tbody></table>'
    return table
