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


from tags.models import Tag


from  tags.forms import TagForm


class TagListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Tag
    paginate_by = 2
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]


class TagDetailView(LoginRequiredMixin, BaseDetailView):
    model = Tag


class TagCreateView(LoginRequiredMixin, FormMixin,
                    SuccessUrlMixin, BaseCreateView):
    model = Tag
    form_class = TagForm


class TagUpdateView(LoginRequiredMixin, FormMixin,
                    SuccessUrlMixin, BaseUpdateView):
    model = Tag
    form_class = TagForm


class TagDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Tag
