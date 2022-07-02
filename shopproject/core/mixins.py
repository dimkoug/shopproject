from django.urls import reverse_lazy
from django.shortcuts import redirect


class ModelMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['app'] = self.model._meta.app_label
        context['model'] = self.model
        context['model_name'] = self.model.__name__.lower()
        title = self.model.__name__.capitalize()
        if 'List' in self.__class__.__name__:
            title += ' List'
        if 'Detail' in self.__class__.__name__:
            title += ' Detail'
        if 'Create' in self.__class__.__name__:
            title += ' Create'
        if 'Update' in self.__class__.__name__:
            title += ' Update {}'.format(self.get_object())
        if 'Delete' in self.__class__.__name__:
            title += ' Delete {}'.format(self.get_object())
        context['page_title'] = title
        return context


class FormMixin:
    def form_valid(self, form):
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
        return reverse_lazy('{}:{}-list'.format(
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

        context.update({'pages': pages})
        return context
