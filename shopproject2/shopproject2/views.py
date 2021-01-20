from django.views.generic import TemplateView
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from products.models import Product, Specification, Attribute

from core.functions import id_generator
from core.pagination import get_pagination


class HomeView(TemplateView):
    template_name = "index.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('cart_id'):
             self.request.session['cart_id'] = id_generator(256)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        attrs = self.request.GET.getlist('attrs')
        print(attrs)
        products = Product.status.published()
        if attrs:
            products = products.filter(attributes__in=attrs)
        context['attrs_checked'] = attrs
        context['product_list'] = get_pagination(self.request, products,
            settings.PRODUCT_LIST_ITEMS)
        context['specification_list'] = Specification.objects.prefetch_related(
            Prefetch('attributes', queryset=Attribute.objects.select_related(
                'specification'))).filter(is_published=True)
        return context
