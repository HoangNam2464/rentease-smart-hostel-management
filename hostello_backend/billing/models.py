import calendar
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from contracts.models import Contract
from properties.models import Room


MONEY_ZERO = Decimal('0.00')


class PriceConfig(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='price_configs')
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    electricity_unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    water_unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    service_fee = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    effective_from = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cau_hinh_gia'
        ordering = ['-year', '-month', 'room__room_code']
        verbose_name = 'Price Config'
        verbose_name_plural = 'Price Configs'
        constraints = [
            models.UniqueConstraint(fields=['room', 'month', 'year'], name='unique_price_config_per_room_month'),
        ]
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['year', 'month']),
            models.Index(fields=['room', 'year', 'month']),
        ]

    def __str__(self):
        return f'{self.room} - {self.month:02d}/{self.year}'


class Invoice(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_UNPAID = 'unpaid'
    STATUS_PARTIAL = 'partial'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_UNPAID, 'Unpaid'),
        (STATUS_PARTIAL, 'Partial'),
        (STATUS_PAID, 'Paid'),
        (STATUS_OVERDUE, 'Overdue'),
    )

    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name='invoices')
    invoice_code = models.CharField(max_length=80, unique=True, blank=True)
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    issued_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, validators=[MinValueValidator(0)])
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hoa_don'
        ordering = ['-year', '-month', 'contract__contract_code']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        constraints = [
            models.UniqueConstraint(fields=['contract', 'month', 'year'], name='unique_invoice_per_contract_month'),
        ]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['year', 'month']),
            models.Index(fields=['due_date']),
            models.Index(fields=['contract']),
        ]

    def __str__(self):
        return self.invoice_code or f'Invoice {self.month:02d}/{self.year}'

    def build_invoice_code(self):
        if not self.contract_id:
            return ''
        room_code = self.contract.room.room_code
        return f'INV-{self.year}{self.month:02d}-{room_code}'

    def clean(self):
        if self.contract_id and self.month and self.year:
            self.invoice_code = self.invoice_code or self.build_invoice_code()
            self._validate_contract_period()

        if self.issued_date and self.due_date and self.due_date < self.issued_date:
            raise ValidationError({'due_date': 'Due date must be on or after issued date.'})

        if self.paid_amount > self.total_amount:
            raise ValidationError({'paid_amount': 'Paid amount cannot exceed total amount.'})

        expected_remaining = self.total_amount - self.paid_amount
        if expected_remaining < MONEY_ZERO:
            expected_remaining = MONEY_ZERO
        if self.remaining_amount != expected_remaining:
            self.remaining_amount = expected_remaining

    def _validate_contract_period(self):
        month_start = date(self.year, self.month, 1)
        last_day = calendar.monthrange(self.year, self.month)[1]
        month_end = date(self.year, self.month, last_day)

        if month_end < self.contract.start_date or month_start > self.contract.end_date:
            raise ValidationError({
                'month': 'Invoice month must overlap the contract period.',
                'year': 'Invoice year must overlap the contract period.',
            })

    def recalculate_totals(self, commit=True):
        total = getattr(self, 'detail', None).total_line_amount if hasattr(self, 'detail') else self.total_amount
        paid = self.payments.aggregate(total=Sum('amount'))['total'] or MONEY_ZERO
        remaining = total - paid
        if remaining < MONEY_ZERO:
            remaining = MONEY_ZERO

        self.total_amount = total
        self.paid_amount = paid
        self.remaining_amount = remaining
        self.status = self._status_for_amounts()

        if commit:
            self.save(update_fields=['total_amount', 'paid_amount', 'remaining_amount', 'status', 'updated_at'])

    def _status_for_amounts(self):
        if self.total_amount <= MONEY_ZERO and self.paid_amount <= MONEY_ZERO:
            return self.STATUS_DRAFT
        if self.remaining_amount <= MONEY_ZERO:
            return self.STATUS_PAID
        if self.paid_amount > MONEY_ZERO:
            return self.STATUS_PARTIAL
        if self.due_date and self.due_date < timezone.localdate():
            return self.STATUS_OVERDUE
        return self.STATUS_UNPAID

    def save(self, *args, **kwargs):
        if self.contract_id and self.month and self.year and not self.invoice_code:
            self.invoice_code = self.build_invoice_code()
        super().save(*args, **kwargs)


class InvoiceDetail(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='detail')
    electricity_start = models.PositiveIntegerField()
    electricity_end = models.PositiveIntegerField()
    electricity_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, validators=[MinValueValidator(0)])
    water_start = models.PositiveIntegerField()
    water_end = models.PositiveIntegerField()
    water_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, validators=[MinValueValidator(0)])
    electricity_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, editable=False, validators=[MinValueValidator(0)])
    water_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, editable=False, validators=[MinValueValidator(0)])
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, editable=False, validators=[MinValueValidator(0)])
    service_amount = models.DecimalField(max_digits=12, decimal_places=2, default=MONEY_ZERO, editable=False, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'chi_tiet_hoa_don'
        verbose_name = 'Invoice Detail'
        verbose_name_plural = 'Invoice Details'
        indexes = [
            models.Index(fields=['invoice']),
        ]

    @property
    def total_line_amount(self):
        return self.electricity_amount + self.water_amount + self.rent_amount + self.service_amount

    def __str__(self):
        return f'Detail for {self.invoice}'

    def clean(self):
        if self.electricity_end < self.electricity_start:
            raise ValidationError({'electricity_end': 'Electricity ending reading must be greater than or equal to starting reading.'})
        if self.water_end < self.water_start:
            raise ValidationError({'water_end': 'Water ending reading must be greater than or equal to starting reading.'})

        self.populate_snapshot()
        self.calculate_amounts()

    def populate_snapshot(self):
        config = PriceConfig.objects.filter(
            room=self.invoice.contract.room,
            month=self.invoice.month,
            year=self.invoice.year,
        ).first()
        if not config:
            raise ValidationError('Price config is required for this room, month, and year.')

        self.electricity_unit_price = config.electricity_unit_price
        self.water_unit_price = config.water_unit_price
        self.rent_amount = self.invoice.contract.rent_amount
        self.service_amount = config.service_fee

    def calculate_amounts(self):
        electricity_usage = Decimal(self.electricity_end - self.electricity_start)
        water_usage = Decimal(self.water_end - self.water_start)
        self.electricity_amount = electricity_usage * self.electricity_unit_price
        self.water_amount = water_usage * self.water_unit_price

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.invoice.recalculate_totals()


class PaymentHistory(models.Model):
    METHOD_CASH = 'cash'
    METHOD_BANK_TRANSFER = 'bank_transfer'
    METHOD_E_WALLET = 'e_wallet'
    METHOD_OTHER = 'other'

    METHOD_CHOICES = (
        (METHOD_CASH, 'Cash'),
        (METHOD_BANK_TRANSFER, 'Bank Transfer'),
        (METHOD_E_WALLET, 'E-Wallet'),
        (METHOD_OTHER, 'Other'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    method = models.CharField(max_length=30, choices=METHOD_CHOICES, default=METHOD_CASH)
    transaction_code = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(default=timezone.now)
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='collected_payments',
        blank=True,
        null=True,
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lich_su_thanh_toan'
        ordering = ['-paid_at', '-created_at']
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment Histories'
        indexes = [
            models.Index(fields=['invoice']),
            models.Index(fields=['paid_at']),
            models.Index(fields=['method']),
            models.Index(fields=['transaction_code']),
        ]

    def __str__(self):
        return f'{self.invoice} - {self.amount}'

    def clean(self):
        if self.amount <= MONEY_ZERO:
            raise ValidationError({'amount': 'Payment amount must be greater than zero.'})

        if self.invoice_id:
            paid_query = PaymentHistory.objects.filter(invoice_id=self.invoice_id)
            if self.pk:
                paid_query = paid_query.exclude(pk=self.pk)
            already_paid = paid_query.aggregate(total=Sum('amount'))['total'] or MONEY_ZERO
            outstanding = self.invoice.total_amount - already_paid
            if self.amount > outstanding:
                raise ValidationError({'amount': 'Payment amount cannot exceed invoice remaining amount.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.invoice.recalculate_totals()

    def delete(self, *args, **kwargs):
        invoice = self.invoice
        result = super().delete(*args, **kwargs)
        invoice.recalculate_totals()
        return result
