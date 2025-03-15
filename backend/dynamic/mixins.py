from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string

from .functions import create_query_string, is_ajax


class QueryListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        q_objects = Q()
        if q and q != '':
            q = str(q.strip())
            for f in  self.model._meta.get_fields():
                print(f.__class__.__name__)
                if f.__class__.__name__  in ['CharField', 'TextField']:
                    str_q = f"Q({f.name}__icontains='{q}')"
                    print(str_q)
                    q_obj = eval(str_q)
                    print(q_obj)
                    q_objects |= q_obj
            queryset = queryset.filter(q_objects)
        return queryset



class ModelMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        model = self.model
        app = model._meta.app_label
        model_name = model.__name__.lower()
        title = model._meta.verbose_name_plural.capitalize()
        # back_url = reverse("{}-list".format(model_name))
        # create_url = reverse("{}-create".format(model_name))
        # setattr(self, 'back_url', back_url)
        # setattr(self, 'create_url', create_url)
        if hasattr(self, 'ajax_partial'):
            context['template'] = self.ajax_partial
        context['app'] = app
        context['model'] = model
        context['model_name'] = model_name
        # context['back_url'] = back_url
        # context['create_url'] = create_url
        context['page_title'] = title
        context['query_string'] = create_query_string(self.request)
        return context


class AjaxListMixin:
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if is_ajax(request):
            data = serializers.serialize("json", self.object_list)
            return JsonResponse(data, safe=False)
        context = self.get_context_data()
        return self.render_to_response(context)


class AjaxFormMixin:
    def form_valid(self, form):
        form.save()
        if is_ajax(self.request):
            data = serializers.serialize("json", [form.instance])
            return JsonResponse(data, safe=False, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)


class FormCreateMixin:
    def get_success_url(self):
        return self.list_url
    
    def form_valid(self, form):
        model_name = self.kwargs.get('model_name')
        form.save()
        if 'continue' in self.request.POST:
            try:
                url = reverse_lazy('{}:change'.format(
                form.instance._meta.app_label),
                kwargs={'pk': form.instance.pk,"model_name":form.instance.__name__.lower()})
            except NoReverseMatch:
                url = reverse_lazy('change'.format(
                form.instance._meta.app_label),
                kwargs={'pk': form.instance.pk,"model_name":form.instance.__name__.lower()})
            return redirect(url)
        if 'new' in self.request.POST:
            try:
                url = reverse_lazy('{}:add'.format(
                form.instance._meta.app_label),
                kwargs={"model_name":form.instance.__name__.lower()})
            except NoReverseMatch:
                url = reverse_lazy('add'.format(
                form.instance._meta.app_label),
                kwargs={"model_name":form.instance.__name__.lower()})
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)


class FormUpdateMixin:
    def get_success_url(self):
        return self.list_url
    
    def form_valid(self, form):
        model_name = self.kwargs.get('model_name')
        form.save()
        if 'continue' in self.request.POST:
            try:
                url = reverse_lazy('{}:change'.format(
                form.instance._meta.app_label),
                kwargs={'pk': form.instance.pk,"model_name":form.instance.__name__.lower()})
            except NoReverseMatch:
                url = reverse_lazy('change'.format(
                form.instance._meta.app_label),
                kwargs={'pk': form.instance.pk,"model_name":form.instance.__name__.lower()})
            return redirect(url)
        if 'new' in self.request.POST:
            try:
                url = reverse_lazy('{}:add'.format(
                form.instance._meta.app_label),
                kwargs={"model_name":form.instance.__name__.lower()})
            except NoReverseMatch:
                url = reverse_lazy('add'.format(
                form.instance._meta.app_label),
                kwargs={"model_name":form.instance.__name__.lower()})
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)


class SuccessUrlMixin:
    def get_success_url(self):
        url = ''
        model_name = self.model.__name__.lower()
        try:
            url = reverse('{}:list'.format(
                self.model._meta.app_label),kwargs={"model_name":model_name})
        except NoReverseMatch:
            url = reverse('list',kwargs={"model_name":model_name})
        return url


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PaginationMixin:
    def get_paginate_by(self, queryset):
        # Check for page size in URL query parameters
        page_size = self.request.GET.get('page_size')
        if page_size:
            return int(page_size)
        return self.paginate_by
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_string'] = create_query_string(self.request)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context


class AjaxDeleteMixin:
    def dispatch(self, *args, **kwargs):
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        return super().dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            self.object = self.get_object()
            self.object.delete()
            data = dict()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        return super().get(request, *args, **kwargs)
