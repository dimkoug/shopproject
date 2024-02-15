from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from core.functions import get_rows 


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
                    str_q = f"Q({f.name}__icontains='{str(q)}')"
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
        model_name = self.model.__name__.lower()
        context['app'] = 'cms'
        context['model'] = model
        context['model_name'] = model_name
        # context['fields'] = self.fields
        # table = get_rows(self.fields,super().get_queryset())
        # context['table'] = table
        # fields = []
        # for f in self.model._meta.fields:
        #     fields.append(f.name)
        # context['fields'] = fields
        title = model._meta.verbose_name.capitalize()
        if 'list' in self.__class__.__name__.lower():
            title = model._meta.verbose_name_plural.capitalize()
        if 'detail' in self.__class__.__name__.lower():
            title += ' Detail {}'.format(self.get_object())
        if 'create' in self.__class__.__name__.lower():
            title += ' Create'
        if 'update' in self.__class__.__name__.lower():
            title += ' Update {}'.format(self.get_object())
        if 'delete' in self.__class__.__name__.lower():
            title += ' Delete {}'.format(self.get_object())
        context['page_title'] = title
        back_url = reverse("cms:{}-list".format(model_name))
        create_url = reverse("cms:{}-create".format(model_name))
        context['back_url'] = back_url
        context['create_url'] = create_url
        return context


class FormMixin:
    def form_valid(self, form):
        form.save()
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy('{}:{}-update'.format(
                form.instance._meta.app_label,
                form.instance.__class__.__name__.lower()),
                kwargs={'pk': form.instance.pk}))
        if 'new' in self.request.POST:
            return redirect(reverse_lazy('{}:{}-create'.format(
                form.instance._meta.app_label,
                form.instance.__class__.__name__.lower())))
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse('{}:{}-list'.format(
            self.model._meta.app_label, self.model.__name__.lower()))


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PaginationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        
        if hasattr(self,'fields'):
            context['fields'] = self.fields
            table = get_rows(self.fields,current_page)
            context['table'] = table
        context.update({'pages': pages})
        return context
