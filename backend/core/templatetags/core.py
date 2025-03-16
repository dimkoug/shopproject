import datetime
from decimal import Decimal
import locale
from django import template
from django.db import models
from django.urls import reverse,reverse_lazy, NoReverseMatch, resolve
from django.apps import apps
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = template.Library()
locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')


@register.filter(name='has_group')
def has_group(user_groups, group_name):
    """
    Checks if the user is part of a specific group.
    :param user_groups: list of groups the user belongs to
    :param group_name: group name to check for
    :return: True if the user belongs to the specified group, otherwise False
    """
    return user_groups.filter(name__icontains=group_name).exists()


@register.simple_tag
def format_currency(value):
    return  locale.currency(abs(value), symbol=True,
                            grouping=True,
                            international=False)



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
def generate_sidebar(context):
    request = context['request']
    urls = ""
    app_models = []
    sorted_menu = sorted(settings.SIDEBAR_APPS)
    for app in sorted_menu:
        item = f"""<li><div class='menu' data-bs-toggle="collapse" data-bs-target='#collapse-{app}' aria-expanded='false' aria-controls='collapse-{app}'>{app.capitalize()}</div>
								<ul class='collapse' id='collapse-{app}'>"""
        app_models = list(apps.get_app_config(app).get_models())
        for model in app_models:
            print(model)
            try:
                url_item = reverse_lazy(
                    "{}:{}-list".format(model._meta.app_label, model.__name__.lower()))
            except NoReverseMatch:
                url_item = None
            print(url_item)
        
            if url_item:
                item += f"<li><a href='{url_item}'>{model.__name__.capitalize()}</a></li>"
        item += '</ul></li>'
        urls += item
    return format_html(mark_safe(urls))


@register.simple_tag
def get_boolean_img(value):
    if value:
        return format_html(mark_safe('<i class="bi bi-check-lg"></i>'))
    return format_html(mark_safe('<i class="bi bi-x"></i>'))


@register.simple_tag
def get_model(obj):
    if obj:
        try:
            return obj.__class__.__name__.lower()
        except:
            return obj.__name__.lower()

    return ''


@register.simple_tag
def get_app(obj):
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


@register.inclusion_tag("core/partials/_add_button.html",takes_context=True)
def add_button(context, app=None):
    view = context["view"]
    model = view.model
    if not app:
        app = model._meta.app_label
    
    url = reverse(f"{app}:{model.__name__.lower()}_add")
    return {"url":url}


@register.inclusion_tag("core/partials/_title.html",takes_context=True)
def get_title(context):
    view = context["view"]
    model = view.model
    return {"title":model._meta.verbose_name_plural.capitalize()}

@register.simple_tag
def get_view_url(obj):
    url = reverse(f"{obj._meta.app_label}:{obj.__class__.__name__.lower()}_view",kwargs={"pk":obj.pk})
    return url

@register.simple_tag
def get_change_url(obj):
    url = reverse(f"{obj._meta.app_label}:{obj.__class__.__name__.lower()}_change",kwargs={"pk":obj.pk})
    return url

@register.simple_tag
def get_delete_url(obj):
    url = reverse(f"{obj._meta.app_label}:{obj.__class__.__name__.lower()}_delete",kwargs={"pk":obj.pk})
    return url



@register.simple_tag(takes_context=True)
def get_list_url(context, form, app=None):
    try:
        model = form.instance
        if not app:
            app = model._meta.app_label
        list_url = reverse(f"{app}:{model.__class__.__name__.lower()}_list")
    except:
        if not app:
            model = context['view'].model
            app = model._meta.app_label
        
        list_url = reverse(f"{app}:{model.__name__.lower()}_list")
    return list_url





@register.inclusion_tag("core/partials/_form_buttons.html",takes_context=True)
def get_form_buttons(context, form):
    return {"form":form, "context":context}


@register.simple_tag
def display_data(object):
    """
    Tag to extract and format data from a model instance for dynamic display in templates,
    including handling fields with choices.
    """
    items = {}
    for field in object._meta.fields:
        try:
            # Check if the field has choices
            if field.choices:
                value = getattr(object, f"get_{field.name}_display")()  # Get the display value
            else:
                value = getattr(object, field.name)
                              # Format Decimal
                if isinstance(value, Decimal):
                    value = round(value, 2)  # Adjust rounding precision as needed
                # Format datetime
                elif isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')  # Default datetime format
                # Handle ForeignKey fields
                elif field.remote_field:  # Checks if the field is a ForeignKey
                    value = str(value) if value else None
            items[field.name] = value
        except AttributeError:
            items[field.name] = None  # Handle missing fields gracefully
    return items
