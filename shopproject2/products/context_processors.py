from products.models import Category, Tag


def get_categories(request):
    return {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()
    }
