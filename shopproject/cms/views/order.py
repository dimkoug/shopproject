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
    BaseIndexView, BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.mixins import FormMixin, SuccessUrlMixin
from cms.views.core import CmsListView

from core.functions import is_ajax


from shop.models import (
    Order,
)


from cms.forms import (
    OrderForm, OrderItemFormSet
)


class OrderListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Order
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Billing Address',
        'db_name':'billing_address'
        },
    ]


class OrderDetailView(LoginRequiredMixin, BaseDetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OrderItemFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OrderItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OrderItemFormSet(self.request.POST or None,
                                            instance=self.get_object())
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OrderItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Order


def model_order(request):
    if request.method == 'POST' and is_ajax(request):
        model_name = request.POST['model_name']
        model = apps.get_model('shop', model_name)
        page_id_array = json.loads(request.POST['page_id_array'])
        objs = []
        for index, item in enumerate(page_id_array):
            if model_name == 'childcategory':
                obj = model.objects.get(target=item["pk"],source=item['parent'])
            elif model_name == 'attributefeature':
                obj = model.objects.get(feature=item)
            elif model_name == 'brandsupplier':
                obj = model.objects.get(supplier=item)
            elif model_name == 'featurecategory':
                obj = model.objects.get(category=item)
            else:
                obj = model.objects.get(pk=item["pk"])
            obj.order = index
            objs.append(obj)
            # obj.save()
        model.objects.bulk_update(objs, ['order'])
        return JsonResponse(page_id_array, safe=False)
    return HttpResponse('')
