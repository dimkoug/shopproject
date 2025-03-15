from django.apps import apps
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_allowed_models():
    # Retrieve all models from all apps
    all_models = apps.get_models()

    # Define a list of excluded or included app labels (optional)
    excluded_apps = ['admin', 'auth']  # Example: Exclude default apps
    allowed_models = []

    for model in all_models:
        app_label = model._meta.app_label
        model_name = model.__name__

        # Exclude certain apps if needed
        if app_label not in excluded_apps:
            allowed_models.append((app_label, model_name))

    return allowed_models



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
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


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

def get_data_for_sb(request,app_name, model_name):
    """"
    Return Data for  select box 2  plugin
    """
    if not app_name:
        raise ValueError("App name not provided or invalid")
    if not model_name:
        raise ValueError("Model name not provided or invalid")
    
    model = apps.get_model(app_label=app_name, model_name=model_name)
    
    
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_superuser:
            data = model.objects.filter(q_objects)
        else:
            if hasattr(model, 'user'):
                data = model.objects.select_related('user').filter(q_objects,user_id=request.user.id)
            else:
                data = model.objects.all()
    else:
        if request.user.is_superuser:
            data = model.objects.all()
        else:
            if hasattr(model, 'user'):
                data = model.objects.select_related('user').filter(user_id=request.user.id)
            else:
                data = model.objects.all()
    
    
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)


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
