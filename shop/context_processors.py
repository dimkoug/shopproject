from django.db.models import Prefetch, Count
from shop.models import (
    ShoppingCart, Brand,
    Category, ProductCategory,
    Tag, Hero, HeroItem
)


def get_context_data(request):
    published_products = ProductCategory.objects.select_related(
        'product', 'category').filter(product__price__gt=0)
    active_products = Count('productcategories', filter=published_products)
    third_categories = Category.objects.prefetch_related(
            Prefetch('productcategories',
                     queryset=ProductCategory.objects.select_related('category'))
            ).annotate(count_active_products=Count('productcategories'),
                       c=active_products).filter(
                       productcategories__in=published_products)
    second_categories = Category.objects.prefetch_related('children').filter(
        children__in=third_categories).distinct()
    first_categories = Category.objects.prefetch_related('children').filter(
        children__in=second_categories).distinct()
    shopping_cart_id = request.session.get('shopping_cart_id')
    heroes = Hero.objects.prefetch_related(
        Prefetch('heroitems',
                 queryset=HeroItem.objects.select_related(
                    'product', 'hero').filter(
                        is_published=True), to_attr='item_list'
                 )
        ).filter(is_published=True)
    if shopping_cart_id:
        basket_count = ShoppingCart.objects.filter(
            shopping_cart_id=shopping_cart_id).count()
    else:
        basket_count = 0

    p = Prefetch(
        'children',
        queryset=Category.objects.prefetch_related(
                    Prefetch(
                        'children',
                        queryset=Category.objects.filter(
                             id__in=third_categories).order_by('order'),
                        to_attr='third_level'
                    )
                ).filter(id__in=second_categories).order_by('order'),
        to_attr='second_level'
    )

    categories = Category.objects.prefetch_related(p).filter(
        is_published=True, id__in=first_categories).order_by('order')

    return {
        'categories': categories,
        'tags': Tag.objects.filter(is_published=True),
        'brands': Brand.objects.filter(is_published=True),
        'donottrack': request.META.get('HTTP_DNT') == '1',
        'basket_count': basket_count,
        'heroes': heroes
    }
