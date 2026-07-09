from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import UserProfile


class Property(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Đang hoạt động'),
        (STATUS_INACTIVE, 'Ngừng hoạt động'),
    )

    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='properties')
    property_code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    ward = models.CharField(max_length=100, blank=True)
    province_city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    contact_phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    timezone = models.CharField(max_length=64, default='Asia/Ho_Chi_Minh')
    house_rules = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'co_so_cho_thue'
        ordering = ['owner', 'property_code']
        verbose_name = 'Cơ sở cho thuê'
        verbose_name_plural = 'Cơ sở cho thuê'
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'property_code'],
                name='unique_property_code_per_owner',
            ),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['property_code']),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['property_code']),
        ]

    def __str__(self):
        return f'{self.property_code} - {self.name}'


class Room(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_OCCUPIED = 'occupied'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_INACTIVE = 'inactive'

    STATUS_CHOICES = (
        (STATUS_AVAILABLE, 'Còn trống'),
        (STATUS_OCCUPIED, 'Đã thuê'),
        (STATUS_MAINTENANCE, 'Đang bảo trì'),
        (STATUS_INACTIVE, 'Ngừng sử dụng'),
    )

    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='rooms')
    property = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        related_name='rooms',
    )
    room_code = models.CharField(max_length=50)
    room_name = models.CharField(max_length=100)
    floor = models.IntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    max_occupants = models.PositiveIntegerField(default=1)
    default_rent = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    room_image = models.ImageField(upload_to='rentease/rooms/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'phong'
        ordering = ['owner', 'room_code']
        verbose_name = 'Phòng trọ'
        verbose_name_plural = 'Phòng trọ'
        constraints = [
            models.UniqueConstraint(fields=['property', 'room_code'], name='unique_room_code_per_property'),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['room_code']),
        ]

    def __str__(self):
        return f'{self.room_code} - {self.room_name}'

    def clean(self):
        super().clean()
        if self.owner_id and self.property_id and self.property.owner_id != self.owner_id:
            raise ValidationError({
                'property': 'Property must belong to the same owner as the room.',
            })
