import uuid
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

from profiles.views import ProtectProfile

from core.functions import create_query_string, is_ajax

from core.mixins import (
    PassRequestToFormViewMixin, PaginationMixin, FormMixin
)

from addresses.models import Address
from addresses.forms import SiteAddressForm 


from brands.models import Brand
from baskets.models import Basket
from orders.models import Order, OrderItem


from shop.models import (
    FeatureCategory, Feature, Product, ProductTag,
    Attribute, Media, ProductAttribute, Category,
)

from orders.forms import (
    SiteOrderForm
)


class IndexView(TemplateView):
    template_name = "shop/site/index.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@method_decorator(cache_page(60 * 15), name='dispatch')
@method_decorator(vary_on_cookie,name='dispatch')
class CatalogListView(PaginationMixin, ListView):

    model = Product
    paginate_by = 10  # if pagination is desired
    template_name = 'shop/site/product_list.html'
    ajax_partial = 'shop/partials/product_ajax_list_partial.html'

    # @method_decorator(cache_page(60 * 15))
    # @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response['X-Cache'] = 'HIT' if response.has_header('Expires') else 'MISS'
        return response

    queryset = Product.active_products.select_related('brand', 'parent', 'category').prefetch_related(
        'tags',
        'attributes__feature',
    ).order_by('price')

    def get_queryset(self):
        queryset = super().get_queryset()
        attrs = []
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        brand = self.request.GET.get('brand')
        tag = self.request.GET.get('tag')
        features = [feature for feature in self.request.GET.keys()
                    if feature.startswith('feature')]
        for feature in features:
            attrs.append(self.request.GET.getlist(feature))
        if category:
            queryset = queryset.filter(category=category)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        if tag:
            queryset = queryset.filter(tags__in=[tag])
        if q and q != '':
            queryset = queryset.filter(Q(name__icontains=q) | Q(code__icontains=q))
        if len(attrs) > 0:
            for attr in attrs:
                queryset = queryset.filter(
                    attributes__in=attr)
        if self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gt=self.request.GET.get('min_price'))

        if self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lt=self.request.GET.get('max_price'))
        # return queryset.values('id', 'name', 'brand_id', 'brand__name', 'subtitle', 'description', 'price')
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
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
        attrs = []
        attrs_checked = []
        features = [feature for feature in self.request.GET.keys()
                    if feature.startswith('feature')]
        selected_features = [f.split('-')[1] for f in features]
        context['url'] = reverse_lazy("shop:catalog")
        context['selected_features'] = selected_features
        for feature in features:
            attrs.append(self.request.GET.getlist(feature))
        for arrt in attrs:
            for item in arrt:
                attrs_checked.append(item)
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        if category:
            category_obj = Category.objects.get(id=category)
            context['category'] = category_obj
            products = Product.active_products.filter(category_id=category_obj.pk)
            lowest_price = products.aggregate(Min('price'))['price__min']
            max_price = products.aggregate(Max('price'))['price__max']
        if brand:
            brand = Brand.objects.get(id=brand)
            context['brand'] = brand
            products = Product.active_products.filter(brand_id=brand.pk)
            lowest_price = products.aggregate(Min('price'))['price__min']
            max_price = products.aggregate(Max('price'))['price__max']

        if self.request.GET.get('min_price'):
            context['selected_min_price'] = self.request.GET.get('min_price')

        if self.request.GET.get('max_price'):
            context['selected_max_price'] = self.request.GET.get('max_price')

        context['min_price'] = lowest_price
        context['max_price'] = max_price
        context['attrs_checked'] = attrs_checked
        counter = Count('productattributes', filter=Q(
            products__in=self.get_queryset()))
        features_items = set()
        attribute_items = set()
        # for a in Attribute.objects.all():
        #     if a.name == '-':
        #         a.delete()
        #     if a.name == '---':
        #         a.delete()
        for p in self.get_queryset():
            for a in p.attributes.all():
                features_items.add(a.feature_id)
                attribute_items.add(a.id)

        feature_list = Feature.objects.prefetch_related(Prefetch('featurecategories', queryset=FeatureCategory.objects.select_related('feature', 'category').filter(filter_display=True)), Prefetch('attributes', queryset=Attribute.objects.select_related('feature').filter(id__in=attribute_items, feature_id__in=features_items).annotate(
            product_count=counter), to_attr='attrs')).filter(
            id__in=features_items, featurecategories__filter_display=True,attributes__in=attribute_items).distinct()
        context['specification_list'] = feature_list
        context['products_count'] = self.get_queryset().count()
        context['query_string'] = create_query_string(self.request)
        return context


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    paginate_by = 100  # if pagination is desired
    template_name = 'shop/site/order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('billing_address', 'shipping_address').prefetch_related(
            Prefetch('orderitems',
                     queryset=OrderItem.objects.select_related(
                         'product', 'order')
                     )).filter(billing_address__profile=self.request.user.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderFormView(LoginRequiredMixin, PassRequestToFormViewMixin,
                    FormMixin, CreateView):
    model = Order
    form_class = SiteOrderForm
    template_name = 'shop/site/order_form.html'
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum = 0
        shopping_items = Basket.objects.select_related(
            'product', 'session').filter(session=self.request.session.session_key)
        for item in shopping_items:
            sum += item.product.price
        context['items'] = shopping_items
        context['sum'] = sum
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        sum = self.get_context_data()['sum']
        items = self.get_context_data()['items']
        obj.order_registration = str(uuid.uuid4())[-10:]
        obj.total = sum
        obj.save()
        for item in items:
            detail = OrderItem()
            detail.order = obj
            detail.product = item.product
            detail.quantity = item.quantity
            detail.save()
        Basket.objects.select_related('session').filter(
            session=self.request.session.session_key).delete()
        messages.success(self.request, 'The order is placed successfully!')
        return super().form_valid(form)





@method_decorator(cache_page(60 * 15), name='dispatch')
@method_decorator(vary_on_cookie,name='dispatch')
class CatalogProductDetailView(DetailView):
    model = Product
    template_name = 'shop/site/product_detail.html'
    queryset = Product.objects.select_related('brand', 'parent', 'category').prefetch_related(
        'tags',
        'media',
        'productlogos',
        'attributes__feature',
        'relatedproducts__target'
    )
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response['X-Cache'] = 'HIT' if response.has_header('Expires') else 'MISS'
        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddressCreateView(FormMixin, CreateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'shop/site/address_form.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_anonymous:
            obj.profile = self.request.user.profile
        address_type = self.request.GET.get('addr')
        if address_type is not None:
            address_type = Address.ADDRESS_CHOICES[int(address_type)][0]
            obj.address_type = address_type
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(ProtectProfile, FormMixin, UpdateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'shop/site/address_form.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url


class AddressDeleteView(ProtectProfile, FormMixin, DeleteView):
    model = Address
    template_name = 'shop/site/address_form_confirm_delete.html'

    def get_success_url(self):
        url = reverse_lazy('index')
        return url


def search_items(request):
    search = request.GET.get('term','').strip()
    search_terms = search.split(' ')
    print(search_terms)
    data = []
    if search and search != '':
        posts = Product.objects.select_related('brand', 'parent', 'category').prefetch_related(
        'tags',
        'attributes__feature',
        ).filter(Q(price__gt=0) & Q(is_published=True))
        q = Q()
        for item in search_terms:
            q |= Q(category__name__icontains=item)
            q |= Q(brand__name__icontains=item)
            q |= Q(name__icontains=item)
            q |= Q(attributes__name__icontains=item)
            q |= Q(attributes__feature__name__icontains=item)
        posts = posts.filter(q).values('id', 'name','image').distinct()

        for post in posts:
            print(post)
            d = {}
            d['value'] = reverse("shop:catalog-product-detail", kwargs={"pk":post['id']})
            d['label'] = post['name'],
            d['image'] = request.build_absolute_uri('/media/'+ post['image'])
            data.append(d)

    return JsonResponse({"data":data})