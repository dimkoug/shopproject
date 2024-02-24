def get_context_data(request):
    return {
        'modelapp': ['shop','addresses','orders','baskets','brands','heroes','logos','offers',
                     'shipments','stocks','suppliers','tags','warehouses'],
    }
