import requests
import urllib3
import os
import hashlib
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db.models import Q, Prefetch
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.core import serializers
from django.db.models import Q
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string



from profiles.models import Profile

from core.functions import is_ajax, get_sb_data

from media.models import Media
from logos.models import Logo

from products.models import Category, Feature, Product, ProductMedia, ProductLogo, ProductAttribute, Attribute

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from xhtml2pdf import pisa, default
from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject


# patch background color/image bleeding into other elements
default.DEFAULT_CSS = DEFAULT_CSS.replace("background-color: transparent;", "", 1)
# patch temporary file resolution when loading fonts
pisaFileObject.getNamedFile = lambda self: self.uri


def get_categories_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Category
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_authenicated:
            data = model.objects.filter(q_objects,user_id=request.user.id)
    else:
        if request.user.is_authenticated:
            data = model.objects.filter(user_id=request.user.id)
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)

    
def get_features_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Feature
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_authenicated:
            data = model.objects.filter(q_objects,user_id=request.user.id)
    else:
        if request.user.is_authenticated:
            data = model.objects.filter(user_id=request.user.id)
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)

def get_products_for_sb(request):
    """"
    Return Data for  select box 2  plugin
    """
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Product
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_authenicated:
            data = model.objects.filter(q_objects,user_id=request.user.id)
    else:
        if request.user.is_authenticated:
            data = model.objects.filter(user_id=request.user.id)
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)


def delete_media(request,product_id,media_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    }
    media = Media.objects.get(id=media_id)
    if media.url:
        r = requests.head(media.url, headers=headers, verify=False, stream=True)
        if r.status_code !=200:
            media.delete()
    else:
        ProductMedia.objects.get(product_id=product_id,media_id=media_id).delete()
    return redirect(reverse("products:product_change",kwargs={"pk":product_id}))
    

def delete_logo(request,product_id,logo_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    }
    media = Logo.objects.get(id=logo_id)
    if media.url:
        r = requests.head(media.url, headers=headers, verify=False, stream=True)
        if r.status_code !=200:
            media.delete()
    else:
        ProductLogo.objects.get(product_id=product_id,logo_id=logo_id).delete()
    return redirect(reverse("products:product_change",kwargs={"pk":product_id}))


def delete_attribute(request,product_id,attribute_id):
    ProductAttribute.objects.get(product_id=product_id,attribute_id=attribute_id).delete()
    return redirect(reverse("products:product_change",kwargs={"pk":product_id}))


def create_product_attribute(request,product_id):
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
        attribute,_ = Attribute.objects.get_or_create(user=request.user,feature=feature,value=request.POST['value'],hash=attribute_hash)
        ProductAttribute.objects.get_or_create(product=product,attribute=attribute)
        return redirect(reverse("products:product_change",kwargs={"pk":product.id}))



    return render(request,template_name,context)



def create_feature_attribute(request,feature_id):
    context = {}
    template_name = 'products/add_feature_attribute.html'
    feature = Feature.objects.get(id=feature_id)
    context['feature'] = feature
    if request.method == 'POST':
        feature = Feature.objects.get(id=request.POST['feature'])
        str2hash = f"{feature.name}{request.POST['value']}"
        result = hashlib.md5(str2hash.encode())
        attribute_hash = result.hexdigest()
        attribute,_ = Attribute.objects.get_or_create(user=request.user,feature=feature,value=request.POST['value'],hash=attribute_hash)
        return redirect(reverse("products:feature_change",kwargs={"pk":feature.id}))



    return render(request,template_name,context)





def link_callback(uri, rel):
    print("URI:", uri)
    sUrl = settings.STATIC_URL
    sRoot = os.path.abspath(os.path.join(settings.BASE_DIR, 'static'))
    # mUrl = settings.MEDIA_URL
    # mRoot = settings.MEDIA_ROOT

    # Handle media files
    # if uri.startswith(mUrl):
    #     path = os.path.join(mRoot, uri.replace(mUrl, "").lstrip('/').replace('/', '\\'))
    # Handle static files
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, "").lstrip('/').replace('/', '\\'))
    # else:
    #     raise Exception('Media URI must start with %s or %s' % (sUrl, mUrl))

    print("Resolved Path:", path)

    # Check if the resolved path exists and is a file
    if not os.path.isfile(path):
        raise Exception('File not found at path: %s' % path)

    return path

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    pdf = render_to_pdf('products/product_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product_{}.pdf"'.format(product.id)
        return response
    return HttpResponse("Error generating PDF", status=400)