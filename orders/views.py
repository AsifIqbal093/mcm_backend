from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db import transaction
from django.db.models import Max
from rest_framework.decorators import api_view, permission_classes


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


class BannerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer

    def get_queryset(self):
        latest_banners = (
            Banner.objects
            .values('position')
            .annotate(latest_update=Max('updated_at'))
        )

        filters = [
            {'position': b['position'], 'updated_at': b['latest_update']}
            for b in latest_banners
        ]

        q = models.Q()
        for f in filters:
            q |= models.Q(**f)

        return Banner.objects.filter(q).order_by('position')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-date')[:5]
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)