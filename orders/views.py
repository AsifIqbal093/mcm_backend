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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # Extract data
        product_ids = data.get('product_ids', [])
        order_amount = data.get('order_amount')
        payment_status = data.get('payment_status', 'pending')
        delivery_status = data.get('delivery_status', 'processing')
        delivery_data = data.get('delivery_info', {})

        # Validate products
        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            return Response({"detail": "Invalid or missing products."}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = Order.objects.create(
            user=user,
            order_amount=order_amount,
            payment_status=payment_status,
            delivery_status=delivery_status
        )
        order.products.set(products)

        # Create delivery info
        DeliveryInfo.objects.create(order=order, **delivery_data)

        # Return full order
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
