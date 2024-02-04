
import random
import string
from django.apps import apps
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.utils.safestring import mark_safe
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile, FileField
from decimal import Decimal
from django.utils.html import format_html


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_pagination(request, queryset, items):
    '''
    items: The number for pagination

    return tuple (total_pages, paginated queryset) 
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


def get_sb_data(request):
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
    return JsonResponse({"results": d_objects}, safe=False)


def delete_model(request):
    model_str = request.GET.get('model')
    app_str = request.GET.get('app')
    id = request.GET.get('id')
    model = apps.get_model(app_label=app_str, model_name=model_str)
    try:
        data = model.objects.get(id=id)
        data.delete()
    except model.DoesNotExist:
        pass
    return JsonResponse({}, safe=False)


def get_rows(fields, object_list):
    trs = []
    print('hi')
    table = "<table class='table table-striped'>"
    thead = '<thead><tr>'
    for field in fields:
        thead += f"<th>{field['verbose_name']}</th>"
    thead += '</tr></thead>'    
    table += thead + '<tbody>'
    for obj in object_list:
        app = obj._meta.app_label
        model = obj.__class__.__name__.lower()
        update_url = reverse_lazy(f"{app}:{model}-update",kwargs={"pk":obj.pk})
        delete_url = reverse_lazy(f"{app}:{model}-delete",kwargs={"pk":obj.pk})
        tr = '<tr>'
        for field in fields:
            db_name = field['db_name']
            value = getattr(obj, db_name)
            if isinstance(value, Decimal):
                value = round(value,0)
            if isinstance(value, bool):
                if value:
                    value = format_html(mark_safe('<i class="bi bi-check-lg text-success"></i>'))
                else:
                    value = format_html(mark_safe('<i class="bi bi-x-lg text-danger"></i>'))
            if isinstance(value,ImageFieldFile):
                if value and value.url:
                    value = format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
            tr += '<td>' + str(value) + '</td>'
        tr += f"""<td><a href='{update_url}'>{format_html(mark_safe('<i class="bi bi-pencil-square text-warning" style="font-size:1.5rem;"></i>'))}</a><a href='{delete_url}        'class='delete-tr'>{format_html(mark_safe('<i class="bi bi-x text-danger" style="font-size:1.5rem;"></i>'))}</a></td>"""
        
        tr += '</tr>'
        table += tr
    table += '</tbody></table>'
    return table