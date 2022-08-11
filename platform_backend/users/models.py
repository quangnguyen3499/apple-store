from datetime import timedelta
import secrets
import string
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets

def generate_otp():
    return "".join(secrets.choice(string.digits) for i in range(6))

class User(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=50, choices=Types.choices, null=True, blank=True)
    active_token = models.TextField(null=True, blank=True)
    active_expires_at = models.DateTimeField(default=timezone.now)

    @property
    def is_admin(self):
        return self.type == self.Types.ADMIN

    @property
    def is_customer(self):
        return self.type == self.Types.CUSTOMER

    def generate_otp(self):
        self.otp_code = generate_otp()
        self.otp_expires_at = timezone.now() + timedelta(hours=24)
        self.save()
        return self.otp_code

    def validate_otp(self, otp: str) -> bool:
        if timezone.now() > self.otp_expires_at:
            return False
        if self.otp_code != otp:
            return False
        return True

class Admin(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    date_joined = models.DateTimeField(max_length=(6), null=True, blank=True)

class Customer(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    address = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=254, null=True, blank=True)
    province = models.CharField(max_length=254, null=True, blank=True)
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    date_joined = models.DateTimeField(max_length=(6), null=True, blank=True)

    def create_token(self) -> str:
        active_token = secrets.token_hex(32)
        self.user.active_token = active_token
        self.user.save()
        return active_token
