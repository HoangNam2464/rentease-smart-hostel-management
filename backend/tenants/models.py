from django.conf import settings
from django.db import models


class Tenant(models.Model):
    GENDER_CHOICES = (
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    )
    STATUS_CHOICES = (
        ('active', 'Đang thuê'),
        ('inactive', 'Ngừng thuê'),
        ('blocked', 'Đã khóa'),
    )

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tenant_profile',
        blank=True,
        null=True,
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    citizen_id = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    citizen_id_front = models.ImageField(upload_to='rentease/citizen_ids/', blank=True, null=True)
    citizen_id_back = models.ImageField(upload_to='rentease/citizen_ids/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'khach_thue'
        ordering = ['full_name']
        verbose_name = 'Khách thuê'
        verbose_name_plural = 'Khách thuê'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.full_name


class CoTenant(models.Model):
    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, related_name='co_tenants')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    citizen_id = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'nguoi_o_cung'
        ordering = ['full_name']
        verbose_name = 'Người ở cùng'
        verbose_name_plural = 'Người ở cùng'
        indexes = [
            models.Index(fields=['citizen_id']),
        ]

    def __str__(self):
        return self.full_name
