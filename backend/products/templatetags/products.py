from django import template
from django.urls import reverse_lazy
register = template.Library()


@register.simple_tag(takes_context=True)
def is_checked(context, attr=None):
    attrs_checked = context['attrs_checked']
    if attrs_checked and attr:
        if not str(attr.pk) in attrs_checked:
            return False
        return True
    return False




@register.simple_tag(takes_context=True)
def is_active(context, pk):
    selected = context['selected_features']
    if pk and selected:
        if not str(pk) in selected:
            return 'hide-feature'
        return f'active-feature'
    return 'hide-feature'