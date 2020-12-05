from products.models import (ShoppingCartItem, Brand,
                             Category,ProductCategory, Tag)


def get_context_data(request):
    productcategories = [productcategory.category.id for productcategory
                         in ProductCategory.status.published()]
    cart_id = request.session.get('cart_id')
    if cart_id:
        basket_count = ShoppingCartItem.objects.filter(cartId=cart_id).count()
    else:
        basket_count = 0
    return {
        'categories': Category.objects.filter(id__in=productcategories),
        'tags': Tag.status.published(),
        'brands': Brand.status.published(),
        'basket_count' : basket_count
    }
