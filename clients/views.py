from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Super Admin":
            return Client.objects.all()
        elif user.role == "admin":
            client_ids = ClientUser.objects.filter(user=user).values_list('client_id', flat=True)
            return Client.objects.filter(id__in=client_ids)
        return Client.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "Super Admin":
            raise PermissionDenied("Only Super Admins can create clients.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        client = self.get_object()
        if user.role == "Super Admin":
            serializer.save()
        elif user.role == "admin":
            is_linked = ClientUser.objects.filter(client=client, user=user).exists()
            if not is_linked:
                raise PermissionDenied("You can only update your own client.")
            serializer.save()
        else:
            raise PermissionDenied("Unauthorized.")

    def perform_destroy(self, instance):
        if self.request.user.role != "Super Admin":
            raise PermissionDenied("Only Super Admins can delete clients.")
        instance.delete()


class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all()
    serializer_class = ClientUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Super Admin":
            return ClientUser.objects.all()
        elif user.role == "admin":
            return ClientUser.objects.filter(client__users__user=user)
        return ClientUser.objects.none()

    def get_serializer_class(self):
        # Use the bulk serializer only for the assign-users action
        if self.action == "assign_users":
            return ClientUserBulkAssignSerializer
        return ClientUserSerializer

    @action(detail=False, methods=['post'], url_path='assign-users')
    def assign_users(self, request):
        """
        Assign multiple users to a single client:
        {
          "client": 1,
          "users": [5, 6, 7]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_id = serializer.validated_data['client']
        user_ids = serializer.validated_data['users']

        # Permission check
        if self.request.user.role != "Super Admin":
            is_admin = ClientUser.objects.filter(
                client_id=client_id, user=self.request.user
            ).exists()
            if not is_admin or self.request.user.role != "admin":
                raise PermissionDenied("Only client admins or Super Admins can assign users.")

        client = Client.objects.get(id=client_id)
        created = []
        for uid in user_ids:
            user = User.objects.get(id=uid)
            obj, created_flag = ClientUser.objects.get_or_create(client=client, user=user)
            if created_flag:
                created.append(obj)

        return Response(
            {"message": f"{len(created)} user(s) assigned to client."},
            status=status.HTTP_201_CREATED
        )

class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "Super Admin":
            return ClientAddress.objects.all()
        elif user.role == "admin":
            client_ids = ClientUser.objects.filter(user=user).values_list('client_id', flat=True)
            return ClientAddress.objects.filter(client_id__in=client_ids)
        return ClientAddress.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        client = serializer.validated_data['client']

        if user.role == "Super Admin":
            serializer.save()
        elif user.role == "admin":
            is_admin = ClientUser.objects.filter(client=client, user=user).exists()
            if not is_admin:
                raise PermissionDenied("You can only add addresses to your own client.")
            serializer.save()
        else:
            raise PermissionDenied("Unauthorized.")

    def perform_update(self, serializer):
        self.perform_create(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == "Super Admin":
            instance.delete()
        elif user.role == "admin":
            is_admin = ClientUser.objects.filter(client=instance.client, user=user).exists()
            if not is_admin:
                raise PermissionDenied("You can only delete addresses for your own client.")
            instance.delete()
        else:
            raise PermissionDenied("Unauthorized.")