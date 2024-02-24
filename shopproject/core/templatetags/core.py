import locale
from django import template
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.utils.safestring import mark_safe
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile, FileField
from decimal import Decimal
from django.utils.html import format_html
register = template.Library()

locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')

@register.simple_tag
def format_currency(value):
    return locale.currency(abs(value), symbol=True,
                            grouping=True, international=False)


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
    app = 'cms'
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
    app = 'cms'
    lower_name = model.__name__.lower()
    template_name = "{}/partials/{}_list_partial.html".format(app,lower_name)
    return template_name


@register.simple_tag(takes_context=True)
def get_template_name_cms(context, *args):
    model = context['model']
    app = 'cms'
    lower_name = model.__name__.lower()
    template_name = "cms/partials/{}_list_partial.html".format(lower_name)
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
def is_selected(value, object_list):
    if str(value) in object_list:
        return True
    return False


def sortFn(value):
  return value.__name__


@register.simple_tag(takes_context=True)
def get_generate_sidebar(context):
    request = context['request']
    urls = ""
    cms_apps = []
    model_apps = context['modelapp']
    for model_app in model_apps:
        app_models = list(apps.get_app_config(model_app).get_models())
        cms_apps.extend(app_models)
    cms_apps.sort(key=sortFn)

    for model in cms_apps:
        try:
            url_item = reverse(
                "cms:{}-list".format(model.__name__.lower()))
        except NoReverseMatch:
            url_item = None
        if url_item:
            lower_model_name = model.__name__.lower()
            plural_model_name = model._meta.verbose_name_plural.capitalize()
            item = "<li class='nav-item'><a href='{}'".format(url_item)
            if url_item == request.path:
                item += "class='nav-link active collection'"
            else:
                item += "class='nav-link collection'"
            item +=f"data-model='{lower_model_name}' data-collection='{plural_model_name}'"
            item += ">{}</a></li>".format(plural_model_name)
            print(item)
            urls += item
    return format_html(mark_safe(urls))


@register.simple_tag
def get_rows(fields, object_list):
    trs = []
    for obj in object_list:
        app = obj._meta.app_label
        model = obj.__class__.__name__.lower()
        update_url = reverse(f"cms:{model}-update",kwargs={"pk":obj.pk})
        delete_url = reverse(f"cms:{model}-delete",kwargs={"pk":obj.pk})
        tr = '<tr>'
        for field in fields:
            db_name = field['db_name']
            value = getattr(obj, db_name)
            print(value.__class__.__name__)
            if isinstance(value, Decimal):
                value = round(value,0)
            if isinstance(value, bool):
                if value:
                    value = format_html(mark_safe('<i class="bi bi-check-lg text-success"></i>'))
                else:
                    value = format_html(mark_safe('<i class="bi bi-x-lg text-danger"></i>'))
            if isinstance(value,ImageFieldFile):
                if value and value.url:
                    value = format_html(mark_safe('<img src="{}" width="100px" />'.format(value.url)))
            tr += '<td>' + str(value) + '</td>'
        tr += f"""<td><a href='{update_url}'>{format_html(mark_safe('<i class="bi bi-pencil-square text-warning" style="font-size:1.5rem;"></i>'))}</a><a href='{delete_url}        'class='delete-tr'>{format_html(mark_safe('<i class="bi bi-x text-danger" style="font-size:1.5rem;"></i>'))}</a></td>"""
        
        tr += '</tr>'
        trs.append(tr)
    items = ''
    for i in trs:
        items += str(i)
    return format_html(mark_safe(items))