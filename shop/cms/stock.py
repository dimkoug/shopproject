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


from shop.models import (
    Stock,
)


from shop.forms import (
    StockForm,
)


class StockListView(LoginRequiredMixin, BaseListView):
    model = Stock
    paginate_by = 50


class StockDetailView(LoginRequiredMixin, BaseDetailView):
    model = Stock


class StockCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Stock
    form_class = StockForm


class StockUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Stock
    form_class = StockForm


class StockDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Stock
