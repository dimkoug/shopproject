from django.db.models import Prefetch
from shop.models import (ShoppingCartItem, Brand,
                         Category, ProductCategory, Tag, Hero, HeroItem)


def get_context_data(request):
    productcategories = [productcategory.category.id for productcategory
                         in ProductCategory.status.published()]
    cart_id = request.session.get('shopping_cart_id')
    heroes = Hero.objects.prefetch_related(
        Prefetch('heroitems',
                 queryset=HeroItem.objects.select_related(
                    'product', 'hero').filter(
                        is_published=True), to_attr='item_list'
                 )
        ).filter(is_published=True)
    if cart_id:
        basket_count = ShoppingCartItem.objects.filter(cartid=cart_id).count()
    else:
        basket_count = 0
    return {
        'categories': Category.objects.filter(
            parent__isnull=True, is_published=True),
        'tags': Tag.status.published(),
        'brands': Brand.status.published(),
        'donottrack': request.META.get('HTTP_DNT') == '1',
        'basket_count': basket_count,
        'heroes': heroes
    }
