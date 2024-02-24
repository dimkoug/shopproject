import uuid
from django.db.models import Prefetch, Count


from brands.models import Brand
from tags.models import Tag
from shop.models import (
    Category, Product,
    ChildCategory
)

from baskets.models import Basket
from heroes.models import Hero,HeroItem

def get_context_data(request):
    third_categories = Product.objects.filter(price__gt=0, is_published=True).values_list('category_id',flat=True).distinct()
    second_categories = Category.objects.prefetch_related('children').filter(
        children__in=third_categories).values_list('id',flat=True).distinct()
    first_categories = Category.objects.prefetch_related('children').filter(
        children__in=second_categories).values_list('id',flat=True).distinct()
    heroes = Hero.objects.prefetch_related(
        Prefetch('heroitems',
                 queryset=HeroItem.objects.select_related(
                    'product', 'hero'), to_attr='item_list'
                 )
        ).filter(is_published=True)

    request.session['shopping_cart_id'] = str(uuid.uuid4())


    basket_count = Basket.objects.select_related('session').filter(
        session=request.session.session_key).count()



    p = Prefetch(
        'children',
        queryset=ChildCategory.objects.select_related(
                'source', 'target').prefetch_related(
                    Prefetch(
                        'target__children',
                        queryset=ChildCategory.objects.select_related(
                            'source', 'target').filter(
                             target_id__in=third_categories).order_by('target__order'),
                        to_attr='third_level'
                    )
                ).filter(target_id__in=second_categories).order_by('target__order'),
        to_attr='second_level'
    )


    categories = Category.objects.prefetch_related(p).filter(
        id__in=first_categories, is_published=True).order_by('order').distinct()
    

    return {
        'categories': categories,
        'tags': Tag.objects.filter(is_published=True),
        'brands': Brand.objects.prefetch_related('products').filter(is_published=True,products__price__gt=0,products__is_published=True).order_by('name').distinct(),
        'donottrack': request.META.get('HTTP_DNT') == '1',
        'basket_count': basket_count,
        'heroes': heroes,
        'app': 'shop',
    }
