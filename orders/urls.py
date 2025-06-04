from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, user_order_history, BannerViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'banners', BannerViewSet, basename='banners')


urlpatterns = [
    path('orders/history/', user_order_history, name='user-order-history'),
    path('', include(router.urls)),
]
