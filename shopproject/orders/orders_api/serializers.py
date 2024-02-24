from rest_framework import serializers



from orders.models import Order, OrderItem


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['order_registration', 'billing_address', 'shipping_address', 'total', 'comments']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']