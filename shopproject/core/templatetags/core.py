from django import template
from django.urls import reverse_lazy, resolve
from django.utils.safestring import mark_safe
from django.utils.html import format_html
register = template.Library()


@register.simple_tag(takes_context=True)
def get_url(context, action, obj=None):
    '''
    example 1  " get_url 'list' "
    example 2  " get_url 'create' "
    example 3  " get_url 'detail' obj  "
    the first argument is action create or list or detail or update or delete
    the second argument is a model object
    the name of url pattern so as to work
    app:model-create
    app:model-update
    app:model-delete
    app:model-detail
    '''
    model = context['model']
    lower_name = model.__name__.lower()
    app = model._meta.app_label
    url_string = '{}:{}-{}'.format(app, lower_name, action)
    if obj:
        url = reverse_lazy(url_string, kwargs={'pk': obj.pk})
    if not obj:
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        url = reverse_lazy(url_string)
    return url


@register.simple_tag(takes_context=True)
def get_template_name(context, *args):
    model = context['model']
    app = model._meta.app_label
    lower_name = model.__name__.lower()
    template_name = "{}/partials/{}_list_partial.html".format(app,lower_name)
    return template_name


@register.simple_tag(takes_context=True)
def get_template_name_cms(context, *args):
    model = context['model']
    app = model._meta.app_label
    lower_name = model.__name__.lower()
    template_name = "shop/cms/partials/{}_list_partial.html".format(lower_name)
    return template_name


@register.simple_tag
def get_model(obj):
    return obj.__class__.__name__.lower()


@register.simple_tag
def get_app(obj):
    return obj._meta.app_label


@register.simple_tag
def get_boolean_img(value):
    if value:
        return format_html(mark_safe('<i class="bi bi-check-lg text-success"></i>'))
    return format_html(mark_safe('<i class="bi bi-x-lg text-danger"></i>'))


@register.simple_tag
def get_formset_img(obj, value):
    if value.__class__.__name__ == 'ImageFieldFile' and value:
        return format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
    return ""


@register.simple_tag
def is_active(request , url):
    if  resolve(request.path).url_name == url:
        return 'active'
    return ''


@register.simple_tag
def get_selected_attr(pk, items):
    if pk in items:
        return True
    return False