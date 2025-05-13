from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, DeliveryInfo, Product
from .serializers import OrderSerializer, DeliveryInfoSerializer
from django.db import transaction

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('user', 'delivery_info').prefetch_related('products')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        'payment',
        'status',
        'products__product_name'
    ]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        return self.queryset.filter(user=user)
