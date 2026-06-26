from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from properties.models import Room
from tenants.models import Tenant


class RoomListing(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_HIDDEN = 'hidden'
    STATUS_RENTED = 'rented'
    STATUS_EXPIRED = 'expired'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_RENTED, 'Rented'),
        (STATUS_EXPIRED, 'Expired'),
    )

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    available_from = models.DateField()
    published_at = models.DateTimeField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tin_phong'
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Room Listing'
        verbose_name_plural = 'Room Listings'
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['status']),
            models.Index(fields=['available_from']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return f'{self.title} - {self.room}'

    def clean(self):
        if self.expired_at and self.published_at and self.expired_at < self.published_at:
            raise ValidationError({'expired_at': 'Expired date must not be before published date.'})

        if self.status == self.STATUS_PUBLISHED and self.room_id:
            published_listings = RoomListing.objects.filter(
                room_id=self.room_id,
                status=self.STATUS_PUBLISHED,
            )
            if self.pk:
                published_listings = published_listings.exclude(pk=self.pk)
            if published_listings.exists():
                raise ValidationError({'room': 'This room already has a published listing.'})

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        self.full_clean()
        super().save(*args, **kwargs)


class ViewingRegistration(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_NO_SHOW = 'no_show'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_NO_SHOW, 'No Show'),
    )

    listing = models.ForeignKey(RoomListing, on_delete=models.PROTECT, related_name='viewing_registrations')
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='viewing_registrations',
        blank=True,
        null=True,
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    note = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dang_ky_xem_phong'
        ordering = ['-created_at']
        verbose_name = 'Viewing Registration'
        verbose_name_plural = 'Viewing Registrations'
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['preferred_date']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.full_name} - {self.listing}'

    def clean(self):
        self.phone = self.phone.strip() if self.phone else ''
        if not self.phone:
            raise ValidationError({'phone': 'Phone must not be empty.'})

        if self.preferred_date and self.preferred_date < timezone.localdate():
            raise ValidationError({'preferred_date': 'Preferred date must be today or in the future.'})

        if self.listing_id and self.listing.status != RoomListing.STATUS_PUBLISHED:
            raise ValidationError({'listing': 'Viewing registration must target a published listing.'})

    def populate_tenant_snapshot(self):
        if not self.tenant_id:
            return
        if not self.full_name:
            self.full_name = self.tenant.full_name
        if not self.phone:
            self.phone = self.tenant.phone_number
        if not self.email:
            self.email = self.tenant.email

    def save(self, *args, **kwargs):
        self.populate_tenant_snapshot()
        self.full_clean()
        super().save(*args, **kwargs)
