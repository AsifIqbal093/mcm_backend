"""
Views for user API and related e-commerce models.
"""

from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from user.models import User, Address
from .permissions import IsAdmin
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserAdminSerializer,
    AddressSerializer
)

# ------------------- USER AUTH ------------------- #

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user with role included."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'role': getattr(user, 'role', None),
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return self.queryset.order_by('-date_joined')

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return Address.objects.all()
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            serializer.save()
        elif serializer.instance.user == user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this address.")

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser or instance.user == user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this address.")
