import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.functions import get_pagination



class ManageView(LoginRequiredMixin, TemplateView):
    template_name = "cms/manage.html"



class IndexView(TemplateView):
    template_name = "site/index.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('shopping_cart_id'):
            self.request.session['shopping_cart_id'] = str(uuid.uuid4())
        print('index cart: ', self.request.session['shopping_cart_id'])
        return super().dispatch(*args, **kwargs)











class TestView(TemplateView):
    template_name = "test.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []
        for i in range(800):
            data.append({
                "id": i,
                "name": f"name_{i}"
            })
        paginator,num_pages,current_page = get_pagination(self.request,data,10)
        page_no = current_page.number
        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]
        context.update({'pages': pages})
        context['data'] = current_page
        return context




