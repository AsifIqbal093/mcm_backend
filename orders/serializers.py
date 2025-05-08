from rest_framework import serializers
from .models import Order, DeliveryInfo
from estore.models import Product

class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name']

class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = [
            "recipient_name", "address", "phone_number", "city",
            "postal_code", "country"
        ]


class OrderSerializer(serializers.ModelSerializer):
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True
    )
    products = serializers.SerializerMethodField(read_only=True)
    delivery_info = DeliveryInfoSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product_ids', 'products', 'date',
            'amount', 'delivery_info'
        ]
        read_only_fields = ['amount']

    def get_products(self, obj):
        return [product.product_name for product in obj.products.all()]

    def create(self, validated_data):
        delivery_data = validated_data.pop('delivery_info')
        product_ids = validated_data.pop('product_ids')

        # Calculate total from sale_price
        products = Product.objects.filter(id__in=[p.id for p in product_ids])
        total_amount = sum([p.sale_price or 0 for p in products])

        # Create order with calculated amount
        order = Order.objects.create(
            user=validated_data['user'],
            amount=total_amount,
            payment=validated_data.get('payment', 'pending'),
            status=validated_data.get('status', 'processing')
        )
        order.products.set(product_ids)
        DeliveryInfo.objects.create(order=order, **delivery_data)

        return order


