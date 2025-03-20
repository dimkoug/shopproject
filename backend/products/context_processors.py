import uuid
from django.db.models import Prefetch, Count


from brands.models import Brand
from tags.models import Tag
from products.models import (
    Category, Product,
    ChildCategory
)

from baskets.models import Basket
from heroes.models import Hero,HeroItem


def get_context_data(request):
    # Fetch third-level categories (leaf categories with products)
    third_categories = set(Product.objects.filter(
        price__gt=0, is_published=True
    ).values_list('category_id', flat=True))

    # Fetch second-level categories (parents of third-level categories)
    second_categories = set(Category.objects.filter(
        children__id__in=third_categories
    ).values_list('id', flat=True))

    # Fetch first-level categories (parents of second-level categories)
    first_categories = set(Category.objects.filter(
        children__id__in=second_categories
    ).values_list('id', flat=True))

    # Fetch heroes with prefetching
    heroes = Hero.objects.prefetch_related(
        Prefetch(
            'heroitems',
            queryset=HeroItem.objects.select_related('product', 'hero'),
            to_attr='item_list'
        )
    ).filter(is_published=True, heroitems__isnull=False)

    # Ensure session key exists
    if not request.session.session_key:
        request.session.save()

    # Fetch basket count efficiently
    basket_count = Basket.objects.filter(
        session_key=request.session.session_key
    ).count() if request.session.session_key else 0

    # Optimize category prefetching
    second_level_qs = ChildCategory.objects.filter(
        target_id__in=second_categories
    ).select_related('source', 'target').order_by('order')

    third_level_qs = ChildCategory.objects.filter(
        target_id__in=third_categories
    ).select_related('source', 'target').order_by('order')

    second_level_prefetch = Prefetch(
        'children',
        queryset=second_level_qs.prefetch_related(
            Prefetch('target__children', queryset=third_level_qs, to_attr='third_level')
        ),
        to_attr='second_level'
    )

    # Fetch all categories with prefetching
    categories = Category.objects.prefetch_related(second_level_prefetch).filter(
        id__in=first_categories, is_published=True
    ).order_by('order')

    # Fetch published tags & brands
    tags = Tag.objects.filter(is_published=True)
    
    brands = Brand.objects.prefetch_related('products').filter(
        is_published=True,
        products__price__gt=0,
        products__is_published=True
    ).distinct().order_by('name')

    # Return optimized context data
    return {
        'categories': categories,
        'tags': tags,
        'brands': brands,
        'donottrack': request.META.get('HTTP_DNT') == '1',
        'basket_count': basket_count,
        'heroes': heroes,
        'app': 'shop',
    }