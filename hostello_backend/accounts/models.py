from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    """Custom user model kept backward-compatible for RentEase migration."""
    USER_TYPES = (
        ('ADMIN', 'Admin'),
        ('OWNER', 'Owner'),
        ('TENANT', 'Tenant'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='TENANT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_owner(self):
        return self.user_type == 'OWNER'

    @property
    def is_tenant(self):
        return self.user_type == 'TENANT'

    @property
    def is_rentease_admin(self):
        return self.user_type == 'ADMIN'


class UserProfile(models.Model):
    """RentEase owner/manager profile (NGUOI_DUNG)."""
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rentease_profile')
    full_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='rentease/avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    rental_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nguoi_dung'
        verbose_name = 'Owner Profile'
        verbose_name_plural = 'Owner Profiles'
        indexes = [
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return self.full_name or self.user.username

class WardenProfile(models.Model):
    """Warden Profile - Single warden for the hostel"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='warden_profile')
    designation = models.CharField(max_length=100, default='Hostel Warden')
    department = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='warden_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Warden: {self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "Warden Profile"
        verbose_name_plural = "Warden Profiles"
