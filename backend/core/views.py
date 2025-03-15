from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from core.mixins import *
from core.functions import *

class BaseListView(LoginRequiredMixin,PaginationMixin, ListView):
    def dispatch(self, request, *args, **kwargs):
        model_name = self.model.__name__.lower()
        app_label = self.model._meta.app_label
        self.list_url = reverse_lazy(f"{app_label}:{model_name}_list")
        self.add_url = reverse_lazy(f"{app_label}:{model_name}_add")
        self.title = self.model._meta.verbose_name_plural.capitalize() 
        self.ajax_partial = f"{app_label}/partials/_{model_name}_list.html"
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        if is_ajax(request):
            print(self.ajax_partial)
            template = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse(template,safe=False)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = self.ajax_partial
        context['search'] = self.request.GET.get('search', '')
        context['query_string'] = create_query_string(self.request)
        return context


class BaseDetailView(LoginRequiredMixin, DetailView):
    def dispatch(self, request, *args, **kwargs):
        model_name = self.model.__name__.lower()
        app_label = self.model._meta.app_label
        self.title = self.model._meta.verbose_name.capitalize() + ' Details'
        self.list_url = reverse_lazy(f"{app_label}:{model_name}_list")
        return super().dispatch(request, *args, **kwargs)
    



class BaseCreateView(LoginRequiredMixin, FormMixin,CreateView):
    def dispatch(self, request, *args, **kwargs):
        model_name = self.model.__name__.lower()
        app_label = self.model._meta.app_label
        self.title = self.model._meta.verbose_name.capitalize() + ' Create'
        self.list_url = reverse_lazy(f"{app_label}:{model_name}_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_success_url(self):
        return self.list_url



class BaseUpdateView(LoginRequiredMixin, FormMixin,UpdateView):
    def dispatch(self, request, *args, **kwargs):
        model_name = self.model.__name__.lower()
        app_label = self.model._meta.app_label
        self.title = self.model._meta.verbose_name.capitalize() + ' Update'
        self.list_url = reverse_lazy(f"{app_label}:{model_name}_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_success_url(self):
        return self.list_url


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    def dispatch(self, request, *args, **kwargs):
        model_name = self.model.__name__.lower()
        app_label = self.model._meta.app_label
        self.title = self.model._meta.verbose_name.capitalize() + ' Delete'
        self.list_url = reverse_lazy(f"{app_label}:{model_name}_list")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.list_url
