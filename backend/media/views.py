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

from media.models import Media

from media.forms import MediaForm



class MediaListView(BaseListView):
    model = Media
    paginate_by = 50


class MediaDetailView(BaseDetailView):
    model = Media


class MediaCreateView(BaseCreateView):
    model = Media
    form_class = MediaForm


class MediaUpdateView(BaseUpdateView):
    model = Media
    form_class = MediaForm


class MediaDeleteView(BaseDeleteView):
    model = Media
