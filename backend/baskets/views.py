from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Min ,Max
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Prefetch, Count, Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django import template
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from core.functions import create_query_string, is_ajax

from core.mixins import (
    PassRequestToFormViewMixin, PaginationMixin, FormMixin
)

from baskets.models import Basket



class BasketView(TemplateView):
    template_name = 'baskets/basket.html'
    ajax_partial = 'baskets/partials/basket_partial.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if is_ajax(request):
            context['ajax'] = True
            html = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html': html})
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_cart_id = self.request.session.get('shopping_cart_id')
        sum = 0
        shopping_items = Basket.objects.select_related(
            'product').filter(session_key=self.request.session.session_key)
        for item in shopping_items:
            sum += item.product.price * item.quantity
        context['sum'] = sum
        context['items'] = shopping_items
        return context