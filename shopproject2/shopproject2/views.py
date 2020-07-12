import string
import random
from django.views.generic import TemplateView
from django.db.models import Prefetch
from core.mixins import ProtectedViewMixin

from products.models import Product, Feature, Attribute


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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
        products = Product.objects.all()
        if attrs:
            products = products.filter(attributes__in=attrs)
        context['attrs_checked'] = attrs
        context['product_list'] = products
        context['feature_list'] = Feature.objects.prefetch_related(
            Prefetch('attributes', queryset=Attribute.objects.select_related(
                'feature'))).all()
        return context


class ManageView(ProtectedViewMixin, TemplateView):
    template_name = "manage.html"
