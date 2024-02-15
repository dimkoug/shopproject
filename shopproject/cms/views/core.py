from django.views.generic.list import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse

from core.functions import is_ajax

from core.mixins import QueryListMixin


class CmsListView(QueryListMixin):
    def dispatch(self, *args, **kwargs):
        self.ajax_list_partial = 'cms/partials/{}_list_partial.html'.format(self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_list_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)