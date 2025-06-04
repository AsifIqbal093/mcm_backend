from django.conf import settings
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    nif = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    commercial_discount = models.DecimalField(max_digits=5, decimal_places=2)
    spring_id = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_clients')

    def __str__(self):
        return self.name


class ClientAddress(models.Model):
    client = models.ForeignKey(Client, related_name='addresses', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.city}"


class ClientUser(models.Model):
    client = models.ForeignKey('Client', related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('client', 'user')  # prevent duplicate assignment

    def __str__(self):
        return f"{self.user.email} → {self.client.name}"
