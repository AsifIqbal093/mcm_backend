from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardAnalyticsViewSet

router = DefaultRouter()
router.register(r'dashboard', DashboardAnalyticsViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
