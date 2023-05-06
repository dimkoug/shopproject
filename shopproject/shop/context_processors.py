from django.db.models import Prefetch, Count
from shop.models import (
    ShoppingCart, Brand,
    Category, Product,
    Tag, Hero, HeroItem
)


def get_context_data(request):
    third_categories = Product.objects.values_list('category_id',flat=True).distinct()
    second_categories = Category.objects.prefetch_related('to_categories').filter(
        to_categories__from_category__in=third_categories).values_list('id',flat=True).distinct()
    first_categories = Category.objects.prefetch_related('to_categories').filter(
        to_categories__from_category__in=second_categories).values_list('id',flat=True).distinct()
    shopping_cart_id = request.session.get('shopping_cart_id')
    heroes = Hero.objects.prefetch_related(
        Prefetch('heroitems',
                 queryset=HeroItem.objects.select_related(
                    'product', 'hero'), to_attr='item_list'
                 )
        ).filter(is_published=True)
    if shopping_cart_id:
        basket_count = ShoppingCart.objects.filter(
            shopping_cart_id=shopping_cart_id).count()
    else:
        basket_count = 0

    categories = Category.objects.prefetch_related('to_categories__from_category__to_categories__from_category', 'parents').filter(
        id__in=first_categories, parents__isnull=True).order_by('order').distinct()
    

    return {
        'categories': categories,
        'tags': Tag.objects.filter(is_published=True),
        'brands': Brand.objects.prefetch_related('products').filter(is_published=True,products__isnull=False,products__is_published=True).distinct(),
        'donottrack': request.META.get('HTTP_DNT') == '1',
        'basket_count': basket_count,
        'heroes': heroes
    }
