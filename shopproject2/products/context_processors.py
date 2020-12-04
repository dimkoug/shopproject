from products.models import Category,ProductCategory, Tag


def get_categories(request):
    productcategories = [productcategory.category.id for productcategory
                         in ProductCategory.status.published()]
    return {
        'categories': Category.objects.filter(id__in=productcategories),
        'tags': Tag.status.published()
    }
