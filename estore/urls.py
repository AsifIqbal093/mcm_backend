from rest_framework.routers import DefaultRouter
from estore import views
from django.urls import path, include

router = DefaultRouter()

# Register existing viewsets
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('carts', views.CartViewSet)
router.register('cart-items', views.CartItemViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)
router.register('payments', views.PaymentViewSet)

# Register the UserSettings viewset
router.register('user-settings', views.UserSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
