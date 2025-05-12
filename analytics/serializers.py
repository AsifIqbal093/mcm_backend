from rest_framework import serializers
from orders.models import Order, DeliveryInfo
from estore.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'sale_price']

class SimpleOrderSerializer(serializers.ModelSerializer):
    products = SimpleProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'date', 'amount', 'payment', 'status']