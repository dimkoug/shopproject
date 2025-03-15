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


from brands.models import Brand
from brands.forms import BrandForm


class BrandListView(BaseListView):
    model = Brand
    queryset = Brand.objects.select_related('user')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
        {
        'verbose_name': 'Suppliers',
        'db_name':'suppliers'
        },
        {
        'verbose_name': 'Image',
        'db_name':'image'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier = self.request.GET.get('supplier')
        if supplier and supplier != '':
            queryset = queryset.filter(suppliers=supplier)
        return queryset


class BrandDetailView(BaseDetailView):
    model = Brand


class BrandCreateView(BaseCreateView):
    model = Brand
    form_class = BrandForm

class BrandUpdateView(BaseUpdateView):
    model = Brand
    form_class = BrandForm

class BrandDeleteView( BaseDeleteView):
    model = Brand
