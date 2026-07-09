from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from billing.models import Invoice
from contracts.models import Contract
from properties.models import Room
from tenants.models import Tenant


class RepairRequest(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Thấp'),
        (PRIORITY_MEDIUM, 'Trung bình'),
        (PRIORITY_HIGH, 'Cao'),
        (PRIORITY_URGENT, 'Khẩn cấp'),
    )

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Đang chờ'),
        (STATUS_IN_PROGRESS, 'Đang xử lý'),
        (STATUS_COMPLETED, 'Đã hoàn thành'),
        (STATUS_CANCELLED, 'Đã hủy'),
    )

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='repair_requests')
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='repair_requests',
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='rentease/repair_requests/', blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    requested_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(blank=True, null=True)
    owner_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'yeu_cau_sua_chua'
        ordering = ['-requested_at', '-created_at']
        verbose_name = 'Yêu cầu sửa chữa'
        verbose_name_plural = 'Yêu cầu sửa chữa'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['requested_at']),
            models.Index(fields=['room']),
            models.Index(fields=['tenant']),
        ]

    def __str__(self):
        return f'{self.title} - {self.room}'

    def clean(self):
        if self.status != self.STATUS_COMPLETED and self.resolved_at:
            raise ValidationError({'resolved_at': 'Resolved date is only valid when status is completed.'})

        if self.tenant_id and self.room_id:
            is_related = Contract.objects.filter(room_id=self.room_id, tenant_id=self.tenant_id).exists()
            if not is_related:
                raise ValidationError({'tenant': 'Tenant must be related to this room through a current or historical contract.'})

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_COMPLETED and not self.resolved_at:
            self.resolved_at = timezone.now()
        self.full_clean()
        super().save(*args, **kwargs)


class MaintenanceRecord(models.Model):
    STATUS_SCHEDULED = 'scheduled'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_SCHEDULED, 'Đã lên lịch'),
        (STATUS_IN_PROGRESS, 'Đang thực hiện'),
        (STATUS_COMPLETED, 'Đã hoàn thành'),
        (STATUS_CANCELLED, 'Đã hủy'),
    )

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='maintenance_records')
    repair_request = models.ForeignKey(
        RepairRequest,
        on_delete=models.SET_NULL,
        related_name='maintenance_records',
        blank=True,
        null=True,
    )
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
    )
    vendor_name = models.CharField(max_length=150, blank=True)
    performed_by = models.CharField(max_length=150, blank=True)
    performed_date = models.DateField(null=True, blank=True)
    scheduled_for = models.DateField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bao_tri'
        ordering = ['-scheduled_for', '-created_at']
        verbose_name = 'Lịch bảo trì'
        verbose_name_plural = 'Lịch bảo trì'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['maintenance_type']),
            models.Index(fields=['scheduled_for']),
            models.Index(fields=['room']),
        ]

    def __str__(self):
        return f'{self.maintenance_type} - {self.room}'

    def clean(self):
        if self.repair_request_id and self.room_id and self.repair_request.room_id != self.room_id:
            raise ValidationError({'repair_request': 'Repair request room must match maintenance room.'})
            
        if self.status == self.STATUS_COMPLETED and not self.completed_at:
            raise ValidationError({'completed_at': 'Maintenance record must have a completion time when status is completed.'})
            
        if self.completed_at and self.started_at and self.completed_at < self.started_at:
            raise ValidationError({'completed_at': 'Completion time cannot be before start time.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Notification(models.Model):
    TYPE_GENERAL = 'general'
    TYPE_INVOICE = 'invoice'
    TYPE_PAYMENT = 'payment'
    TYPE_OVERDUE = 'overdue'
    TYPE_REPAIR = 'repair'
    TYPE_MAINTENANCE = 'maintenance'

    NOTIFICATION_TYPE_CHOICES = (
        (TYPE_GENERAL, 'Thông báo chung'),
        (TYPE_INVOICE, 'Hóa đơn'),
        (TYPE_PAYMENT, 'Thanh toán'),
        (TYPE_OVERDUE, 'Quá hạn'),
        (TYPE_REPAIR, 'Sửa chữa'),
        (TYPE_MAINTENANCE, 'Bảo trì'),
    )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        related_name='notifications',
        blank=True,
        null=True,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        related_name='notifications',
        blank=True,
        null=True,
    )
    repair_request = models.ForeignKey(
        RepairRequest,
        on_delete=models.SET_NULL,
        related_name='notifications',
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default=TYPE_GENERAL)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'thong_bao'
        ordering = ['-created_at']
        verbose_name = 'Thông báo'
        verbose_name_plural = 'Thông báo'
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['invoice']),
            models.Index(fields=['repair_request']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.invoice_id and self.tenant_id and self.invoice.contract.tenant_id != self.tenant_id:
            raise ValidationError({'invoice': 'Invoice must belong to the selected tenant.'})

        if self.repair_request_id and self.tenant_id:
            if self.repair_request.tenant_id and self.repair_request.tenant_id != self.tenant_id:
                raise ValidationError({'repair_request': 'Repair request must belong to the selected tenant.'})
            if not self.repair_request.tenant_id:
                is_related = Contract.objects.filter(
                    room_id=self.repair_request.room_id,
                    tenant_id=self.tenant_id,
                ).exists()
                if not is_related:
                    raise ValidationError({'repair_request': 'Selected tenant must be related to the repair request room.'})

    def save(self, *args, **kwargs):
        if self.is_read and not self.read_at:
            self.read_at = timezone.now()
        if not self.is_read:
            self.read_at = None
        self.full_clean()
        super().save(*args, **kwargs)
