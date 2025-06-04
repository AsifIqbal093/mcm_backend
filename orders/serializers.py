from rest_framework import serializers
from .models import *
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


class OrderProductInputSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    delivery_info = DeliveryInfoSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_items = OrderProductInputSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product_items', 'products', 'date',
            'amount', 'delivery_info'
        ]
        read_only_fields = ['amount']

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

    def create(self, validated_data):
        delivery_data = validated_data.pop('delivery_info')
        product_items = validated_data.pop('product_items')

        order = Order.objects.create(
            user=validated_data['user'],
            payment=validated_data.get('payment', 'pending'),
            status=validated_data.get('status', 'processing'),
            amount=0
        )

        total_amount = 0
        for item in product_items:
            product_id = item['product_id'].id
            quantity = item['quantity']

            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError(f"Product with ID {product_id} not found.")
            
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.product_name} (Available: {product.stock})"
                )

            # Update stock and sale quantity
            product.stock -= quantity
            product.sale_quantity += quantity
            product.sold_items += quantity
            product.save()

            OrderProduct.objects.create(order=order, product=product, quantity=quantity)
            total_amount += (product.sale_price or 0) * quantity

        order.amount = total_amount
        order.save()

        DeliveryInfo.objects.create(order=order, **delivery_data)
        return order
    
    def update(self, instance, validated_data):
        delivery_data = validated_data.pop('delivery_info', None)
        product_items = validated_data.pop('product_items', [])

        # Step 1: Rollback previous product quantities
        for op in instance.order_products.all():
            product = Product.objects.filter(id=op.product.id).first()
            if product:
                product.stock += op.quantity
                product.sale_quantity -= op.quantity
                product.save()
        instance.order_products.all().delete()

        # Step 2: Update order fields
        instance.payment = validated_data.get('payment', instance.payment)
        instance.status = validated_data.get('status', instance.status)
        total_amount = 0

        for item in product_items:
            product_id = item['product_id'].id
            quantity = item['quantity']

            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError(f"Product with ID {product_id} not found.")
            
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.product_name} (Available: {product.stock})"
                )

            product.stock -= quantity
            product.sale_quantity += quantity
            product.save()

            OrderProduct.objects.create(order=instance, product=product, quantity=quantity)
            total_amount += (product.sale_price or 0) * quantity

        instance.amount = total_amount
        instance.save()

        # Step 3: Update or create delivery info
        if delivery_data:
            if hasattr(instance, 'delivery_info'):
                for key, value in delivery_data.items():
                    setattr(instance.delivery_info, key, value)
                instance.delivery_info.save()
            else:
                DeliveryInfo.objects.create(order=instance, **delivery_data)

        return instance


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image', 'position']
