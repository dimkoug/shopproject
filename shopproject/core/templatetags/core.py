import datetime
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



@register.simple_tag
def exists_in_items(value, items):
    if not str(value) in items:
        return False
    return True


@register.simple_tag
def pagination_links(current_page, total_pages, num_links=4):
    if(total_pages):
        start = max(current_page - num_links // 2, 1)
        end = min(start + num_links - 1, total_pages)
        if end - start < num_links:
            start = max(end - num_links + 1, 1)
        return range(start, end + 1)
    return 0


@register.simple_tag(takes_context=True)
def get_url(context, action, obj=None, app=None):
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
    if not obj:
        model = context['model']
        lower_name = model.__name__.lower()
        if not app:
            app = model._meta.app_label
    else:
        model = obj
        lower_name = model.__class__.__name__.lower()
        if not app:
            app = model._meta.app_label

    url_string = '{}:{}-{}'.format(app, lower_name, action)
    if obj:
       try:
           url = reverse(url_string, kwargs={'pk': obj.pk})
       except NoReverseMatch:
           url = reverse(url_string, kwargs={'slug': obj.slug})
    if not obj:
        url_string = '{}:{}-{}'.format(app, lower_name, action)
        url = reverse_lazy(url_string)
    return url


@register.simple_tag(takes_context=True)
def get_template_name(context, app=None):
    view = context['view']
    print(view.template)
    template_name = view.template
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


@register.inclusion_tag("core/add_button.html",takes_context=True)
def add_button(context, app=None):
    view = context["view"]
    model = view.model
    if not app:
        app = model._meta.app_label
    
    url = reverse(f"{app}:{model.__name__.lower()}-create")
    return {"url":url}


@register.inclusion_tag("core/title.html",takes_context=True)
def get_title(context):
    view = context["view"]
    model = view.model
    return {"title":model._meta.verbose_name_plural.capitalize()}



@register.inclusion_tag("core/detail_url.html")
def get_detail_url(obj, app=None):
    if not app:
        app = obj._meta.app_label
    url = reverse(f"{app}:{obj.__class__.__name__.lower()}-detail",kwargs={"pk":obj.pk})
    return {"url":url}


@register.inclusion_tag("core/edit_url.html")
def get_edit_url(obj, app=None):
    if not app:
        app = obj._meta.app_label
    url = reverse(f"{app}:{obj.__class__.__name__.lower()}-update",kwargs={"pk":obj.pk})
    return {"url":url}


@register.inclusion_tag("core/delete_url.html")
def get_delete_url(obj, app=None):
    if not app:
        app = obj._meta.app_label
    url = reverse(f"{app}:{obj.__class__.__name__.lower()}-delete",kwargs={"pk":obj.pk})
    return {"url":url}


@register.simple_tag(takes_context=True)
def get_list_url(context, form, app=None):
    try:
        model = form.instance
        if not app:
            app = model._meta.app_label
        list_url = reverse(f"{app}:{model.__class__.__name__.lower()}-list")
    except:
        if not app:
            model = context['view'].model
            app = model._meta.app_label
        try:
            list_url = reverse(f"{app}:{model.__name__.lower()}-list")
        except:
            list_url = reverse(f"{app}:{model.__class__.__name__.lower()}-list")
    
    return list_url




@register.inclusion_tag("core/form_buttons.html",takes_context=True)
def get_form_buttons(context, form, app=None):
    return {"form":form,"app":app, "context":context}


@register.simple_tag
def display_data(object):
    items = {}
    for field in object._meta.fields:
        print(type(field), field.name)
        value = getattr(object,field.name)
        if isinstance(value, Decimal):
            value = round(value,0)
        if isinstance(value, datetime.datetime):
            format = '%Y-%m-%d %H:%M:%S'
            print(format)
            # applying strftime() to format the datetime
            string = value.strftime(format)
            value = str(string)
        items[field.name] = value
    return items