import datetime
from decimal import Decimal
from django import template
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = template.Library()

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




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
def get_template_name(context, app=None):
    template_name = context['template']
    return template_name

def sortFn(value):
  return value.__name__


@register.simple_tag(takes_context=True)
def get_generate_sidebar(context):
    request = context['request']
    urls = ""
    app_models = list(apps.get_app_config(context['app']).get_models())
    app_models.sort(key=sortFn)
    
    for model in app_models:
        try:
            url_item = reverse(
                "{}:{}-list".format(model._meta.app_label, model.__name__.lower()))
        except NoReverseMatch:
            url_item = None
        if url_item:
            item = "<div><a href='{}'".format(url_item)
            if url_item == request.path:
                item += "class='active'"
            item += ">{}</a></div>".format(model._meta.verbose_name_plural.capitalize())
            print(item)
            urls += item
    return format_html(mark_safe(urls))


@register.simple_tag
def get_boolean_img(value):
    if value:
        return format_html(mark_safe('<i class="bi bi-check-lg"></i>'))
    return format_html(mark_safe('<i class="bi bi-x"></i>'))


@register.simple_tag
def get_model_name(obj):
    if obj:
        try:
            return obj.__class__.__name__.lower()
        except:
            return obj.__name__.lower()

    return ''


@register.simple_tag
def get_model_app(obj):
    if obj:
        return obj._meta.app_label
    return ''


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
def get_rows(fields, object_list):
    trs = []
    for obj in object_list:
        app = obj._meta.app_label
        model = obj.__class__.__name__.lower()
        update_url = reverse_lazy(f"{app}:{model}_change",kwargs={"pk":obj.pk})
        delete_url = reverse_lazy(f"{app}:{model}_delete",kwargs={"pk":obj.pk})
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


@register.inclusion_tag("partials/_add_button.html",takes_context=True)
def add_button(context):
    view = context["view"]
    model = view.model
    url = reverse(f"dynamic_add",kwargs={"model_name":model.__name__.lower(), 'app_name':model._meta.app_label})
    return {"url":url}


@register.inclusion_tag("partials/_title.html",takes_context=True)
def get_title(context):
    view = context["view"]
    model = view.model
    return {"title":model._meta.verbose_name_plural.capitalize()}


@register.inclusion_tag("partials/_actions.html",takes_context=True)
def get_actions(context, obj):
    view = context["view"]
    model = view.model
    change_url = reverse(f"dynamic_change",kwargs={"pk":obj.pk,"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    delete_url = reverse(f"dynamic_delete",kwargs={"pk":obj.pk,"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    return {"change_url":change_url,"delete_url":delete_url}


@register.simple_tag(takes_context=True)
def get_list_url(context, obj):
    list_url = reverse_lazy(f"dynamic_list",kwargs={"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    return list_url


@register.simple_tag
def get_change_url(obj, app=None):
    url = reverse(f"dynamic_change",kwargs={"pk":obj.pk,"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    return url

@register.simple_tag
def get_delete_url(obj, app=None):
    url = reverse(f"dynamic_delete",kwargs={"pk":obj.pk,"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    return url

@register.simple_tag
def get_view_url(obj, app=None):
    url = reverse(f"dynamic_view",kwargs={"pk":obj.pk,"model_name":obj.__class__.__name__.lower(),"app_name":obj._meta.app_label})
    return url



@register.inclusion_tag("partials/_form_buttons.html",takes_context=True)
def get_form_buttons(context, form):
    return {"form":form, "context":context}


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
