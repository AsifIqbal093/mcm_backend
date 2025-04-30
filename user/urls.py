"""
URL mappings for the user API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

app_name = 'user'

# Create the router and register viewsets if needed
router = DefaultRouter()
# Example: router.register(r'profile', views.UserProfileViewSet, basename='profile')
# Only include this if you are using a ViewSet

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
