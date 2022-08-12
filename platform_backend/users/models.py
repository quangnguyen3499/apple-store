from datetime import timedelta
import secrets
import string
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import uuid
from rest_framework.permissions import BasePermission

def generate_otp():
    return "".join(secrets.choice(string.digits) for i in range(6))

class User(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=50, choices=Types.choices, null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    active_expires_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING, db_index=True
    )

    @property
    def is_admin(self):
        return self.type == self.Types.ADMIN

    @property
    def is_customer(self):
        return self.type == self.Types.CUSTOMER

    def validate_token(self) -> bool:
        if timezone.now() > self.active_expires_at:
            return False
        return True

    def generate_token(self) -> str:
        self.token = secrets.token_hex(32)
        self.active_expires_at = timezone.now() + timedelta(hours=24)
        self.save()
        return self.token

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    date_joined = models.DateTimeField(max_length=(6), null=True, blank=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    address = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=254, null=True, blank=True)
    province = models.CharField(max_length=254, null=True, blank=True)
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    date_joined = models.DateTimeField(max_length=(6), null=True, blank=True)

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")

class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id            
        is_allowed_user = True
        token = request.auth.decode("utf-8")
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
