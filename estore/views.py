from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from rest_framework.permissions import BasePermission, SAFE_METHODS
from estore.models import UserSettings
from estore.serializers import UserSettingsSerializer
from estore.models import Category, Product, Cart, CartItem, Order, OrderItem, Payment

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from estore.serializers import RecentOrderDashboardSerializer
from django.utils import timezone
from datetime import timedelta


from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer
from rest_framework.authentication import TokenAuthentication


from estore.serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    PaymentSerializer,
    UserSettingsSerializer,
    RecentOrderDashboardSerializer
)

# ------------------- CUSTOM PERMISSIONS ------------------- #

class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access to admin users.
    Allow only safe methods (GET, HEAD, OPTIONS) for others.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, 'role', '').lower() == 'admin'

# ------------------- CATEGORY ------------------- #

class CategoryViewSet(viewsets.ModelViewSet):
    """Manage product categories."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


# ------------------- CLIENT ------------------- #
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
# ------------------- PRODUCT ------------------- #

class ProductViewSet(viewsets.ModelViewSet):
    """Manage products."""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


# ------------------- CART ------------------- #

class CartViewSet(viewsets.ModelViewSet):
    """Manage user cart."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------- CART ITEM ------------------- #

class CartItemViewSet(viewsets.ModelViewSet):
    """Manage items in cart."""
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


# ------------------- ORDER ------------------- #

class OrderViewSet(viewsets.ModelViewSet):
    """Manage orders."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------- ORDER ITEM ------------------- #

class OrderItemViewSet(viewsets.ModelViewSet):
    """Manage items in orders."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


# ------------------- PAYMENT ------------------- #

class PaymentViewSet(viewsets.ModelViewSet):
    """Manage payment records."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ------------------- SETTING ------------------- #

class UserSettingsViewSet(viewsets.ModelViewSet):
    """
    Manage user settings.
    """
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        """
        Filter queryset to return only the settings of the authenticated user.
        """
        return UserSettings.objects.filter(user=self.request.user)
    

# ------------------- DASHBOARD RECENT ORDERS ------------------- #

class DashboardRecentOrdersView(APIView):
    """
    Return the last 5 recent orders for the dashboard, with their items and payment info.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
        serializer = RecentOrderDashboardSerializer(recent_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)