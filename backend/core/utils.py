import decimal
from django.apps import apps
from django.db import connections
from django.http import JsonResponse, HttpResponse

from .functions import is_ajax


def dictfetchall(cursor):
    """Return all rows from a cursor as a list of dicts, converting DECIMAL to string while handling NULL values."""
    columns = [col[0] for col in cursor.description]
    print(columns)
    return [
        {col: (str(value) if isinstance(value, decimal.Decimal) else value) if value is not None else None 
         for col, value in zip(columns, row)}
        for row in cursor.fetchall()
    ]

def run_raw_query_on_db(db_name, sql_query):
    print(db_name)
    print(sql_query)
    
    with connections[db_name].cursor() as cursor:
        cursor.execute(sql_query)
        results = dictfetchall(cursor)
    
    return results



def delete_item(request):
    id = request.GET.get('id')
    if not id:
        return JsonResponse({}, safe=False)
    model = request.GET.get('model')
    app = request.GET.get('app')
    model_obj = apps.get_model(app_label=app, model_name=model)
    model_obj.objects.get(id=id).delete()
    return JsonResponse({'message': 'deleted'}, safe=False)


def model_order(request):
    if request.method == 'POST' and is_ajax(request):
        model_name = request.POST['model_name']
        app_name = request.POST['app']
        model = apps.get_model(app_name, model_name)
        page_id_array = request.POST.getlist('page_id_array[]')
        objs = []
        for index, item in enumerate(page_id_array):
            obj = model.objects.get(pk=item)
            obj.order = index
            objs.append(obj)
        model.objects.bulk_update(objs, ['order'])
        return JsonResponse(page_id_array, safe=False)
    return HttpResponse('')