"""
Database models.
"""
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
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.role = "User"
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
        user.role = "Admin"
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=[('Admin', 'Admin'), ('User', 'User')])

    objects = UserManager()

    USERNAME_FIELD = 'email'
