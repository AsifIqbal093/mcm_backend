from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from django.db.models import Sum, F
from estore.permissions import IsAdminUserRole
from user.models import User
from orders.models import Order, OrderProduct
from estore.models import Product
from .serializers import SimpleOrderSerializer

class DashboardAnalyticsViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        today = now().date()
        last_30_days = today - timedelta(days=30)

        client_count = User.objects.filter(role='user').count()

        daily_orders = Order.objects.filter(date__date=today)
        daily_sales_total = daily_orders.aggregate(total=Sum('amount'))['total'] or 0
        daily_orders_data = SimpleOrderSerializer(daily_orders, many=True).data

        last_30_orders = Order.objects.filter(date__date__gte=last_30_days)
        last_30_sales = last_30_orders.aggregate(total=Sum('amount'))['total'] or 0
        last_30_orders_data = SimpleOrderSerializer(last_30_orders, many=True).data

        brand_sales = (
            OrderProduct.objects
            .filter(order__date__gte=last_30_days)
            .values(brand_name=F('product__brand__brand_name'))
            .annotate(total_sales=Sum(F('quantity') * F('product__sale_price')))
            .order_by('-total_sales')[:4]
        )

        total_brand_sales = sum(item['total_sales'] or 0 for item in brand_sales) or 1

        top_brands_percentages = [
            {
                'brand': item['brand_name'],
                'sales': round(item['total_sales'] or 0, 2),
                'percentage': round((item['total_sales'] or 0) * 100 / total_brand_sales, 2)
            }
            for item in brand_sales
        ]
        weekly_sales = []
        for i in range(7):
            day = today - timedelta(days=i)
            day_orders = Order.objects.filter(date__date=day)
            total = day_orders.aggregate(total=Sum('amount'))['total'] or 0
            weekly_sales.append({
                'date': day.strftime('%Y-%m-%d'),
                'sales': round(total, 2)
            })

        weekly_sales.reverse()

        return Response({
            'active_clients': client_count,
            'daily_sales': round(daily_sales_total, 2),
            'daily_orders': daily_orders_data,
            'last_30_days': {
                'total_sales': round(last_30_sales, 2),
                'orders': last_30_orders_data
            },
            'weekly_sales': weekly_sales,
            'top_4_brands': top_brands_percentages
        })
