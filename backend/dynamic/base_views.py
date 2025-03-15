from importlib import import_module
from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from dynamic.functions import *
from dynamic.mixins import *


class BaseListView(LoginRequiredMixin, ListView):
    template_name = 'dynamic/list.html'
    
    def dispatch(self, *args, **kwargs):
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        if self.model:
            self.ajax_partial = '{}/partials/_{}_list.html'.format(self.model._meta.app_label,self.model.__name__.lower())
            self.list_url = reverse("dynamic-list",kwargs={"model_name":model_name, "app_name":app_name})
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        if is_ajax(request):
            print(self.ajax_partial)
            template = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse(template,safe=False)
        return self.render_to_response(context)



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = self.ajax_partial
        context['search'] = self.request.GET.get('search','')
        return context


class BaseDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dynamic/detail.html'
    def dispatch(self, *args, **kwargs):
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        if self.model:
            self.ajax_partial = '{}/partials/_{}_list.html'.format(self.model._meta.app_label,self.model.__name__.lower())
            self.list_url = reverse("dynamic-list",kwargs={"model_name":model_name, "app_name":app_name})
        return super().dispatch(*args, **kwargs)
    


class BaseCreateView(LoginRequiredMixin, FormCreateMixin, CreateView):
    template_name = 'dynamic/form.html'
    def dispatch(self, *args, **kwargs):
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        if self.model:
            self.list_url = reverse("dynamic-list",kwargs={"model_name":model_name, "app_name":app_name})
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    
    def get_form_class(self):
        """
        Dynamically get the form class based on the model name.
        """
        model_name = self.kwargs.get('model_name').capitalize()  # Match naming conventions (e.g., Warehouse -> WarehouseForm)
        form_class_name = f"{model_name}Form"  # Form class name, e.g., WarehouseForm

        try:
            # Dynamically import the module containing forms
            app_module = import_module(f'{self.model._meta.app_label}.forms')

            # Get the form class dynamically
            form_class = getattr(app_module, form_class_name, None)
            if not form_class:
                raise ValueError(f"No form class '{form_class_name}' found in warehouses.forms.")
            
            return form_class  # Return the form class (not an instance)

        except ImportError:
            raise ValueError(f'Error {self.model._meta.app_label}.forms')
    
    def get_model(self):
        allwed = False
        model_name = self.kwargs.get('model_name')
        allowed_models = get_allowed_models()
        print(allowed_models)
        if model_name:
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    return model
        for item in allowed_models:
            if model_name.capitalize() == item[1]:
                allwed = True
        if not allwed:
            raise ValueError("Invalid model name")
        raise ValueError("Model name not provided or invalid")


class BaseUpdateView(LoginRequiredMixin, FormUpdateMixin, UpdateView):
    template_name = 'dynamic/form.html'
    def dispatch(self, *args, **kwargs):
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        if self.model:
            self.list_url = reverse("dynamic-list",kwargs={"model_name":model_name, "app_name":app_name})
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        if model_name:
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    queryset = self.model.objects.all()

                    # Filter objects by user if `user` field exists
                    if hasattr(self.model, 'user') and not self.request.user.is_superuser:
                        queryset = queryset.filter(user_id=self.request.user.id)

                    return queryset

        raise ValueError("Model name not provided or invalid")

    def get_form_class(self):
        """
        Dynamically get the form class based on the model name.
        """
        model_name = self.kwargs.get('model_name').capitalize()  # Match naming conventions (e.g., Warehouse -> WarehouseForm)
        form_class_name = f"{model_name}Form"  # Form class name, e.g., WarehouseForm

        try:
            # Dynamically import the module containing forms
            app_module = import_module(f'{self.model._meta.app_label}.forms')

            # Get the form class dynamically
            form_class = getattr(app_module, form_class_name, None)
            if not form_class:
                raise ValueError(f"No form class '{form_class_name}' found in warehouses.forms.")
            
            return form_class  # Return the form class (not an instance)

        except ImportError:
            raise ValueError(f'Error {self.model._meta.app_label}.forms')

    def get_form(self, form_class=None):
        """
        Dynamically instantiate the form with the object instance.
        """
        if form_class is None:
            form_class = self.get_form_class()

        # Use self.get_form_kwargs() to include the instance automatically
        form_kwargs = self.get_form_kwargs()  # This already includes the 'instance'
        return form_class(**form_kwargs)

    def get_model(self):
        allwed = False
        model_name = self.kwargs.get('model_name')
        allowed_models = get_allowed_models()
        print(allowed_models)
        if model_name:
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    return model
        for item in allowed_models:
            if model_name.capitalize() == item[1]:
                allwed = True
        if not allwed:
            raise ValueError("Invalid model name")
        raise ValueError("Model name not provided or invalid")




class BaseDeleteView(LoginRequiredMixin, SuccessUrlMixin, DeleteView):
    template_name = 'dynamic/delete.html'
    def dispatch(self, *args, **kwargs):
        model_name = self.kwargs.get('model_name')
        app_name = self.kwargs.get('app_name')
        self.model = apps.get_model(app_label=app_name, model_name=model_name)
        if self.model:
            self.list_url = reverse("dynamic-list",kwargs={"model_name":model_name, "app_name":app_name})
        return super().dispatch(*args, **kwargs)
    

    def get_model(self):
        allwed = False
        model_name = self.kwargs.get('model_name')
        allowed_models = get_allowed_models()
        print(allowed_models)
        if model_name:
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    return model
        for item in allowed_models:
            if model_name.capitalize() == item[1]:
                allwed = True
        if not allwed:
            raise ValueError("Invalid model name")
        raise ValueError("Model name not provided or invalid")
    
   

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        if model_name:
            for model in apps.get_models():
                if model.__name__.lower() == model_name.lower():
                    self.model = model
                    queryset = self.model.objects.all()

                    # Filter objects by user if `user` field exists
                    if hasattr(self.model, 'user') and not self.request.user.is_superuser:
                        queryset = queryset.filter(user_id=self.request.user.id)

                    return queryset

        raise ValueError("Model name not provided or invalid")