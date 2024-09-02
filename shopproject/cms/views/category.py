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


from shop.models import Category

from cms.forms import CategoryForm


class CategoryListView(BaseListView):
    model = Category
    queryset = Category.objects.prefetch_related('children', 'targets').filter(targets__isnull=True)
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
        {
        'verbose_name': 'Children',
        'db_name':'children'
        },
    ]


class CategoryDetailView(BaseDetailView):
    model = Category
    queryset = Category.objects.prefetch_related('children')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for c in self.get_object().children.all().order_by('order'):
            print(c, c.order)
        context['categories'] = ''
        return context

class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm





class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(BaseDeleteView):
    model = Category
