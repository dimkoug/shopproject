from django import template
from django.urls import reverse_lazy
register = template.Library()


@register.simple_tag(takes_context=True)
def is_checked(context, attr=None):
    attrs_checked = context['attrs_checked']
    print(attrs_checked)
    print(attr)
    if attrs_checked and attr:
        if not str(attr.pk) in attrs_checked:
            return False
        return True
    return False
