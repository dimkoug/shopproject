import uuid
from django.db.models.query import QuerySet
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Min ,Max
from django.core.cache import cache
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


import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from core.views import *

from logos.models import Logo
from media.models import Media



from products.models import *


from products.forms import *


from core.functions import create_query_string, is_ajax

from core.mixins import (
    PassRequestToFormViewMixin, PaginationMixin, FormMixin
)

from addresses.models import Address
from addresses.forms import SiteAddressForm 


from brands.models import Brand
from baskets.models import Basket
from orders.models import Order, OrderItem


from products.models import *
from orders.forms import (
    SiteOrderForm
)


class AttributeListView(BaseListView):
    model = Attribute
    queryset = Attribute.objects.select_related('feature')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Feature',
        'db_name':'feature'
        },
        {
        'verbose_name': 'Name',
        'db_name':'value'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        feature = self.request.GET.get('feature')
        if feature and feature != '':
            queryset = queryset.filter(feature_id=feature)
        return queryset


class AttributeDetailView(BaseDetailView):
    model = Attribute


class AttributeCreateView(BaseCreateView):
    model = Attribute
    form_class = AttributeForm


class AttributeUpdateView(BaseUpdateView):
    model = Attribute
    form_class = AttributeForm


class AttributeDeleteView(BaseDeleteView):
    model = Attribute


def create_attribute(request,product_id):
    context = {}
    template_name = 'products/add_attribute.html'
    product = Product.objects.get(id=product_id)
    features = Feature.objects.filter(categories=product.category_id).distinct()
    context['features'] = features
    context['product'] = product
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['product_id'])
        feature = Feature.objects.get(id=request.POST['feature'])
        str2hash = f"{feature.name}{request.POST['value']}"
        result = hashlib.md5(str2hash.encode())
        attribute_hash = result.hexdigest()
        ProductAttribute.objects.filter(attribute__feature_id=feature.id,product=product).delete()
        attribute,_ = Attribute.objects.get_or_create(feature=feature,value=request.POST['value'],hash=attribute_hash)
        ProductAttribute.objects.get_or_create(product=product,attribute=attribute)
        return redirect(reverse("cms:product-update",kwargs={"pk":product.id}))
    return render(request,template_name,context)


def delete_attribute(request):
    try:
        feature_id = request.POST['feature']
        attribute = request.POST['attribute']
        product_attribute = Attribute.objects.get(feature_id=feature_id,id=attribute)
        product_attribute.delete()
    except:
        pass
    return JsonResponse({})


class CategoryListView(BaseListView):
    model = Category
    queryset = Category.objects.prefetch_related('children', 'targets').filter(targets__isnull=True)
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
        {
        'verbose_name': 'Children',
        'db_name':'children'
        },
    ]


class CategoryDetailView(BaseDetailView):
    model = Category
    queryset = Category.objects.prefetch_related(Prefetch('children',queryset=ChildCategory.objects.select_related('target').order_by('order')), Prefetch('featurecategories',queryset=FeatureCategory.objects.select_related('feature').order_by('order')))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for c in self.get_object().children.all().order_by('order'):
            print(c, c.order)
        context['categories'] = ''
        return context

class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm





class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(BaseDeleteView):
    model = Category



class FeatureListView(BaseListView):
    model = Feature
    queryset = Feature.objects.prefetch_related('categories').order_by('order')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Feature',
        'db_name':'name'
        },
        {
            'verbose_name': 'Order',
            'db_name': 'order'
        },
        {
        'verbose_name': 'Categories',
        'db_name':'categories'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        print(category)
        if category and category != '':
            queryset = queryset.filter(categories=category)
        return queryset


class FeatureDetailView(BaseDetailView):
    model = Feature
    queryset = Feature.objects.prefetch_related(Prefetch('featurecategories',queryset=FeatureCategory.objects.select_related('category'),to_attr='categorylist'), 'attributes').order_by('order')


class FeatureCreateView(BaseCreateView):
    model = Feature
    form_class = FeatureForm

class FeatureUpdateView(BaseUpdateView):
    model = Feature
    form_class = FeatureForm
    queryset = Feature.objects.prefetch_related(Prefetch('featurecategories',queryset=FeatureCategory.objects.select_related('category'),to_attr='categorylist'), 'attributes').order_by('order')


class FeatureDeleteView(BaseDeleteView):
    model = Feature


def create_featurecategory(request):
    try:
        feature_id = request.POST['feature']
        category_id = request.POST['category']
        filter_display = bool(request.POST.get('filter_display'))
        product_attribute, created = FeatureCategory.objects.update_or_create(feature_id=feature_id,category_id=category_id,defaults={"is_filter":filter_display})
        return JsonResponse({
            'id':product_attribute.id,
            'feature':product_attribute.feature_id,
            'category': product_attribute.category.name,
            'category_id': product_attribute.category_id,
            'is_filter':product_attribute.filter_display
        })
    except Exception as e:
        print(e)
        raise
        return JsonResponse({})

def delete_featurecategory(request):
    try:
        feature_id = request.POST['feature']
        category_id = request.POST['category']
        FeatureCategory.objects.filter(feature_id=feature_id,category_id=category_id).delete()
    except:
        raise
    return JsonResponse({})


class ProductListView(BaseListView):
    model = Product
    paginate_by = 50
    queryset = Product.objects.select_related('brand', 'category').order_by('order')
    fields = [
        {
        'verbose_name': 'Image',
        'db_name':'image'
        },
        {
            'verbose_name': 'Order',
            'db_name': 'order'
        },
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
        {
        'verbose_name': 'Brand',
        'db_name':'brand'
        },
        {
        'verbose_name': 'Code',
        'db_name':'code'
        },
        {
        'verbose_name': 'Category',
        'db_name':'category'
        },
        {
        'verbose_name': 'Published',
        'db_name':'is_published'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        print(category)
        if category and category != '':
            queryset = queryset.filter(category=category)
        if brand and brand != '':
            queryset = queryset.filter(brand=brand)
        return queryset


class ProductDetailView(BaseDetailView):
    model = Product


class ProductCreateView(BaseCreateView):
    model = Product
    form_class = ProductForm



class ProductUpdateView(BaseUpdateView):
    model = Product
    form_class = ProductForm
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('category__featurecategories', 'attributes','tags','relatedproducts')


    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            logos = self.request.FILES.getlist('logos')
            if logos:
                for f in logos:
                    l = Logo()
                    l.image = f
                    l.save()
                    ProductLogo.objects.get_or_create(product=self.get_object(),logo=l)
                    print("logo saved")
            media = self.request.FILES.getlist('media')
            if media:
                for m in media:
                    l = Media()
                    l.image = m
                    l.save()
                    ProductMedia.objects.get_or_create(product=self.get_object(),media=l)
                    print("media saved")
        return super().form_valid(form)


class ProductDeleteView(BaseDeleteView):
    model = Product





class IndexView(TemplateView):
    template_name = "site/index.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@method_decorator(cache_page(60 * 15), name='dispatch')
@method_decorator(vary_on_cookie,name='dispatch')
class CatalogListView(PaginationMixin, ListView):

    model = Product
    paginate_by = 12  # if pagination is desired
    template_name = 'site/product_list.html'
    ajax_partial = 'products/partials/_product_ajax_list.html'

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
        object_list_cache_key = f'object_list_{hash(frozenset(self.request.GET.items()))}'
        object_list = cache.get(object_list_cache_key)
        if not object_list:
            if hasattr(self,'object_list'):
                return self.object_list
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
            self.object_list = queryset
            cache.set(object_list_cache_key, self.object_list, 60 * 15)
        return self.object_list

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
        queryset = self.object_list
        attrs_checked = []
        features = [feature for feature in self.request.GET.keys()
                    if feature.startswith('feature')]
        selected_features = [f.split('-')[1] for f in features]
        context['url'] = reverse_lazy("products:catalog")
        context['selected_features'] = selected_features
        for feature in features:
            attrs.append(self.request.GET.getlist(feature))
        for arrt in attrs:
            for item in arrt:
                attrs_checked.append(item)
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        lowest_price = queryset.aggregate(Min('price'))['price__min']
        max_price = queryset.aggregate(Max('price'))['price__max']
        if category:
            category_obj = Category.objects.get(id=category)
            context['category'] = category_obj
            # products = Product.active_products.filter(category_id=category_obj.pk)
            # lowest_price = products.aggregate(Min('price'))['price__min']
            # max_price = products.aggregate(Max('price'))['price__max']
        if brand:
            brand = Brand.objects.get(id=brand)
            context['brand'] = brand
            # products = Product.active_products.filter(brand_id=brand.pk)
            # lowest_price = products.aggregate(Min('price'))['price__min']
            # max_price = products.aggregate(Max('price'))['price__max']

        if self.request.GET.get('min_price'):
            context['selected_min_price'] = self.request.GET.get('min_price')

        if self.request.GET.get('max_price'):
            context['selected_max_price'] = self.request.GET.get('max_price')

        context['min_price'] = lowest_price
        context['max_price'] = max_price
        context['attrs_checked'] = attrs_checked
        counter = Count('productattributes', filter=Q(
            products__in=queryset))
        features_items = set()
        attribute_items = set()
        # for a in Attribute.objects.all():
        #     if a.name == '-':
        #         a.delete()
        #     if a.name == '---':
        #         a.delete()
        for p in queryset:
            for a in p.attributes.all():
                features_items.add(a.feature_id)
                attribute_items.add(a.id)
        
        feature_cache_key = f'feature_list_{hash(frozenset(self.request.GET.items()))}'
        feature_list = cache.get(feature_cache_key)
        if not feature_list:
            feature_list = Feature.objects.prefetch_related(Prefetch('featurecategories', queryset=FeatureCategory.objects.select_related('feature', 'category').filter(is_filter=True)), Prefetch('attributes', queryset=Attribute.objects.select_related('feature').filter(id__in=attribute_items, feature_id__in=features_items).annotate(
                product_count=counter), to_attr='attrs')).filter(
                id__in=features_items, featurecategories__is_filter=True,attributes__in=attribute_items).distinct()
            cache.set(feature_cache_key, feature_list, 60 * 15)
        
        context['specification_list'] = feature_list
        context['products_count'] = queryset.count()
        context['query_string'] = create_query_string(self.request)
        return context


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    paginate_by = 100  # if pagination is desired
    template_name = 'site/order_list.html'

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
    template_name = 'site/order_form.html'
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
    template_name = 'site/product_detail.html'
    queryset = Product.objects.select_related('brand', 'parent', 'category').prefetch_related(
        'tags',
        'productmedia__media',
        'productlogos__logo',
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


class SiteAddressCreateView(FormMixin, CreateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'site/address_form.html'

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


class SiteAddressUpdateView(FormMixin, UpdateView):
    model = Address
    form_class = SiteAddressForm
    template_name = 'site/address_form.html'

    def get_queryset(self):
        return super().get_queryset().select_related('profile').filter(profile=self.request.user.profile)


    def get_success_url(self):
        url = reverse_lazy('index')
        return url


class SiteAddressDeleteView(FormMixin, DeleteView):
    model = Address
    template_name = 'site/address_form_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().select_related('profile').filter(profile=self.request.user.profile)

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
            q |= Q(attributes__value__icontains=item)
            q |= Q(attributes__feature__name__icontains=item)
        posts = posts.filter(q).values('id', 'name','image').distinct()

        for post in posts:
            print(post)
            d = {}
            d['value'] = reverse("products:catalog-product-detail", kwargs={"pk":post['id']})
            d['label'] = post['name'],
            d['image'] = request.build_absolute_uri('/media/'+ post['image'])
            data.append(d)

    return JsonResponse({"data":data})