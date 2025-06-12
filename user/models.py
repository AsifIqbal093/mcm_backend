from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError('User must have an email!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password):
        """Create, save and return a super user."""
        if not email:
            raise ValueError('User must have an email!')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.role = "Super Admin"
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        """Create, save and return a admin user."""
        if not email:
            raise ValueError('User must have an email!')
        user = self.create_user(email, password)
        user.is_superuser = False
        user.role = "admin"
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password):
        """Create, save and return a admin user."""
        if not email:
            raise ValueError('User must have an email!')
        user = self.create_user(email, password)
        user.is_superuser = False
        user.role = "staff"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    contact_number = models.CharField(max_length=20, blank=True, null=True)
    ammount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_count = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')], default='user')
    nif = models.CharField(max_length=50, blank=True, null=True, unique=False)
    company = models.CharField(blank=True, null=True, unique=False, max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.city}"