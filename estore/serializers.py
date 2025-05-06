# ---------------- New Model Serializers ---------------- #
from rest_framework import serializers
from estore.models import UserSettings
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Payment, Client

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['id', 'user', 'full_name', 'display_name', 'role', 'address', 'bio']


# --- Dashboard-Specific Serializers ---

class DashboardProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']

class DashboardOrderItemSerializer(serializers.ModelSerializer):
    product = DashboardProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class DashboardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'transaction_id', 'payment_method', 'payment_date']

class RecentOrderDashboardSerializer(serializers.ModelSerializer):
    items = DashboardOrderItemSerializer(many=True, read_only=True)
    payment = DashboardPaymentSerializer(source='payment', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'items', 'payment']
