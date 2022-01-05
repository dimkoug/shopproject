import uuid
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = "site/index.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('shopping_cart_id'):
            self.request.session['shopping_cart_id'] = str(uuid.uuid4())
        print('index cart: ', self.request.session['shopping_cart_id'])
        return super().dispatch(*args, **kwargs)


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = "cms/manage.html"
