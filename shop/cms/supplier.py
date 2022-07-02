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

from core.functions import is_ajax


from shop.models import Supplier


from shop.forms import SupplierForm


class SupplierListView(LoginRequiredMixin, BaseListView):
    model = Supplier
    paginate_by = 50


class SupplierDetailView(LoginRequiredMixin, BaseDetailView):
    model = Supplier


class SupplierCreateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseCreateView):
    model = Supplier
    form_class = SupplierForm


class SupplierUpdateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseUpdateView):
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Supplier
