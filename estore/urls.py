from rest_framework.routers import DefaultRouter
from estore import views
from django.urls import path, include

router = DefaultRouter()

# Register existing viewsets
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('brands', views.BrandViewSet)

router.register('clients', views.ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
