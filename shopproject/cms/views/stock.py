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


from stocks.models import Stock


from stocks.forms import StockForm


class StockListView(BaseListView):
    model = Stock
    paginate_by = 50


class StockDetailView(BaseDetailView):
    model = Stock


class StockCreateView(BaseCreateView):
    model = Stock
    form_class = StockForm


class StockUpdateView(BaseUpdateView):
    model = Stock
    form_class = StockForm


class StockDeleteView(BaseDeleteView):
    model = Stock
