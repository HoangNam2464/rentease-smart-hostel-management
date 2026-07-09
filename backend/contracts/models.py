from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from properties.models import Room
from tenants.models import Tenant


class Contract(models.Model):
    PAYMENT_CYCLE_CHOICES = (
        ('monthly', 'Theo tháng'),
        ('yearly', 'Theo năm'),
    )
    STATUS_CHOICES = (
        ('draft', 'Bản nháp'),
        ('active', 'Đang hiệu lực'),
        ('expired', 'Đã hết hạn'),
        ('terminated', 'Đã chấm dứt'),
    )

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='contracts')
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='contracts')
    previous_contract = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='renewals',
        blank=True,
        null=True,
    )
    contract_code = models.CharField(max_length=50, unique=True)
    signed_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    payment_cycle = models.CharField(max_length=20, choices=PAYMENT_CYCLE_CHOICES, default='monthly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hop_dong'
        ordering = ['-start_date', 'contract_code']
        verbose_name = 'Hợp đồng'
        verbose_name_plural = 'Hợp đồng'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date must be after start date.'})

        if self.status == 'active' and self.room_id:
            qs = Contract.objects.filter(room_id=self.room_id, status='active')
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'room': 'This room already has an active contract.'})

    def __str__(self):
        return self.contract_code
