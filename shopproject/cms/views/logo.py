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


from logos.models import Logo


from logos.forms import LogoForm


class LogoListView(BaseListView):
    model = Logo
    paginate_by = 50


class LogoDetailView(BaseDetailView):
    model = Logo


class LogoCreateView(BaseCreateView):
    model = Logo
    form_class = LogoForm


class LogoUpdateView(BaseUpdateView):
    model = Logo
    form_class = LogoForm


class LogoDeleteView(BaseDeleteView):
    model = Logo
