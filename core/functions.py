from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_pagination(request, queryset, items):
    '''
    items: The number for pagination

    return tuple (total_pages, paginated queryset) 
    '''
    paginator = Paginator(queryset, items)
    page = request.GET.get('page')
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    return (paginator, paginator.num_pages, items_page)
