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
    
    def get_products(self, obj):
        return [
            {
                'product_name': op.product.product_name,
                'quantity': op.quantity,
                'unit_price': op.product.sale_price,
                'total_price': op.get_total_price()
            }
            for op in obj.order_products.all()
        ]


class AnalyticsOrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'date', 'amount', 'payment', 'status']

    def get_products(self, obj):
        return [
            {
                'product_name': op.product.product_name,
                'quantity': op.quantity,
                'unit_price': op.product.sale_price,
                'total_price': op.get_total_price()
            }
            for op in obj.order_products.all()
        ]
