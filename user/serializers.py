"""
Serializers for the user API view.
"""
from .models import User, Address
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from orders.models import Order
from django.db.models import Sum, Count

# ---------------- User Serializers ---------------- #

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street_address', 'city', 'country', 'postal_code', 'is_default']


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'password', 'full_name', 'role', 'bio', 'display_name',
            'contact_number', 'addresses'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        user = get_user_model().objects.create_user(**validated_data)
        for address in addresses_data:
            Address.objects.create(user=user, **address)
        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if addresses_data is not None:
            instance.addresses.all().delete()
            for address in addresses_data:
                Address.objects.create(user=instance, **address)

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserAdminSerializer(serializers.ModelSerializer):
    total_order_amount = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'contact_number', 'is_active',
            'total_order_amount', 'total_orders'
        ]

    def get_total_order_amount(self, obj):
        return Order.objects.filter(user=obj).aggregate(total=Sum('amount'))['total'] or 0

    def get_total_orders(self, obj):
        return Order.objects.filter(user=obj).count()
