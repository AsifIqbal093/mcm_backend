from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', ClientViewSet, basename='clients') 
router.register(r'client-users', ClientUserViewSet, basename='client-users')
router.register(r'client-address', ClientAddressViewSet, basename='client-address')

urlpatterns = [
    path('', include(router.urls)),
]
