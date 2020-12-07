from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Prefetch
from core.mixins import ProtectedViewMixin
# Create your views here.

class ManageView(ProtectedViewMixin, TemplateView):
    template_name = "manage.html"
