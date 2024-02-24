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


@register.simple_tag(takes_context=True)
def get_template_name_cms(context, *args):
    model = context['model']
    app = 'cms'
    lower_name = model.__name__.lower()
    template_name = "cms/partials/{}_list_partial.html".format(lower_name)
    return template_name