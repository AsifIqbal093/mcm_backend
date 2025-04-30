# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework import permissions, authentication
# from rest_framework.permissions import BasePermission, SAFE_METHODS
# from estore.models import Category, Product, Cart, CartItem, Order, OrderItem, Payment

# from estore.serializers import (
#     CategorySerializer,
#     ProductSerializer,
#     CartSerializer,
#     CartItemSerializer,
#     OrderSerializer,
#     OrderItemSerializer,
#     PaymentSerializer,
# )

# class IsAdminOrReadOnly(BasePermission):
#     """
#     Allow full access to Admin users.
#     Allow only GET (SAFE_METHODS) for regular users.
#     """

#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False
#         if request.method in SAFE_METHODS:
#             return True
#         return getattr(request.user, 'role', '') == 'Admin'

# # Create your views here.
# # ------------------- CATEGORY ------------------- #

# class CategoryViewSet(viewsets.ModelViewSet):
#     """Manage product categories."""
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     authentication_classes = [authentication.TokenAuthentication]


# # ------------------- PRODUCT ------------------- #

# class ProductViewSet(viewsets.ModelViewSet):
#     """Manage products."""
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# # ------------------- CART ------------------- #

# class CartViewSet(viewsets.ModelViewSet):
#     """Manage user cart."""
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# # ------------------- CART ITEM ------------------- #

# class CartItemViewSet(viewsets.ModelViewSet):
#     """Manage items in cart."""
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objects.filter(cart__user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save()


# # ------------------- ORDER ------------------- #

# class OrderViewSet(viewsets.ModelViewSet):
#     """Manage orders."""
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# # ------------------- ORDER ITEM ------------------- #

# class OrderItemViewSet(viewsets.ModelViewSet):
#     """Manage items in orders."""
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return OrderItem.objects.filter(order__user=self.request.user)


# # ------------------- PAYMENT ------------------- #

# class PaymentViewSet(viewsets.ModelViewSet):
#     """Manage payment records."""
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Payment.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from rest_framework.permissions import BasePermission, SAFE_METHODS

from estore.models import Category, Product, Cart, CartItem, Order, OrderItem, Payment

from estore.serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    PaymentSerializer,
)

# ------------------- CUSTOM PERMISSIONS ------------------- #

class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access to Admin users.
    Allow only GET (SAFE_METHODS) for regular users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, 'role', '') == 'Admin'


# ------------------- CATEGORY ------------------- #

class CategoryViewSet(viewsets.ModelViewSet):
    """Manage product categories."""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
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
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

