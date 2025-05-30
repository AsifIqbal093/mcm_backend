"""
Serializers for the user API view.
"""
from .models import User
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from orders.models import Order
from django.db.models import Sum, Count

# ---------------- User Serializers ---------------- #

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'full_name', 'role', 'address', 'bio', 'display_name', 'contact_number']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

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
