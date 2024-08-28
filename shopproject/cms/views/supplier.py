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

from cms.cms_views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.functions import is_ajax


from suppliers.models import Supplier


from suppliers.forms import SupplierForm


class SupplierListView(BaseListView):
    model = Supplier
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]

class SupplierDetailView(BaseDetailView):
    model = Supplier


class SupplierCreateView(BaseCreateView):
    model = Supplier
    form_class = SupplierForm


class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(BaseDeleteView):
    model = Supplier
