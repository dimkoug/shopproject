import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from core.views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.functions import is_ajax


from orders.models import Order


from orders.forms import OrderForm


class OrderListView(BaseListView):
    model = Order
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Billing Address',
        'db_name':'billing_address'
        },
    ]


class OrderDetailView(BaseDetailView):
    model = Order


class OrderCreateView(BaseCreateView):
    model = Order
    form_class = OrderForm


class OrderUpdateView(BaseUpdateView):
    model = Order
    form_class = OrderForm


class OrderDeleteView(BaseDeleteView):
    model = Order


def model_order(request):
    if request.method == 'POST' and is_ajax(request):
        model_name = request.POST['model_name']
        app_name = request.POST['app_name']
        model = apps.get_model(app_name, model_name)
        page_id_array = json.loads(request.POST['page_id_array'])
        objs = []
        for index, item in enumerate(page_id_array):
            # if model_name == 'childcategory':
            #     obj = model.objects.get(target=item["pk"],source=item['parent'])
            # elif model_name == 'attributefeature':
            #     obj = model.objects.get(feature=item)
            # elif model_name == 'brandsupplier':
            #     obj = model.objects.get(supplier=item)
            # elif model_name == 'featurecategory':
            #     obj = model.objects.get(category=item)
            # else:
            obj = model.objects.get(pk=item["pk"])
            obj.order = index
            objs.append(obj)
            # obj.save()
        model.objects.bulk_update(objs, ['order'])
        return JsonResponse(page_id_array, safe=False)
    return HttpResponse('')
