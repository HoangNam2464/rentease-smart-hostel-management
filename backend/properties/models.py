from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import UserProfile


class Room(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('inactive', 'Inactive'),
    )

    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name='rooms')
    room_code = models.CharField(max_length=50)
    room_name = models.CharField(max_length=100)
    floor = models.IntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    max_occupants = models.PositiveIntegerField(default=1)
    default_rent = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    room_image = models.ImageField(upload_to='rentease/rooms/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'phong'
        ordering = ['owner', 'room_code']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'room_code'], name='unique_room_code_per_owner'),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['room_code']),
        ]

    def __str__(self):
        return f'{self.room_code} - {self.room_name}'
