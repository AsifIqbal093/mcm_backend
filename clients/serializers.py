from rest_framework import serializers
from .models import Client, ClientAddress, ClientUser
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientUserSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ClientUser
        fields = ['id', 'user', 'user_email', 'client']

class ClientUserBulkAssignSerializer(serializers.Serializer):
    client = serializers.IntegerField()
    users = serializers.ListField(child=serializers.IntegerField())



class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        exclude = ['client']


class ClientSerializer(serializers.ModelSerializer):
    addresses = ClientAddressSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'nif', 'telephone', 'commercial_discount', 'spring_id', 'addresses']

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        client = Client.objects.create(**validated_data)
        for address_data in addresses_data:
            ClientAddress.objects.create(client=client, **address_data)
        return client

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.addresses.all().delete()
        for address_data in addresses_data:
            ClientAddress.objects.create(client=instance, **address_data)

        return instance
