import calendar
from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone

from contracts.models import Contract
from properties.models import Property, Room


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


class ServiceDefinition(models.Model):
    CHARGE_FIXED = 'fixed'
    CHARGE_USAGE = 'usage'

    CHARGE_METHOD_CHOICES = (
        (CHARGE_FIXED, 'Fixed'),
        (CHARGE_USAGE, 'Usage-based'),
    )

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='service_definitions')
    service_code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    charge_method = models.CharField(max_length=20, choices=CHARGE_METHOD_CHOICES)
    unit = models.CharField(max_length=30)
    default_unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=MONEY_ZERO,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dinh_nghia_dich_vu'
        ordering = ['property', 'service_code']
        verbose_name = 'Service Definition'
        verbose_name_plural = 'Service Definitions'
        constraints = [
            models.UniqueConstraint(
                fields=['property', 'service_code'],
                name='unique_service_code_per_property',
            ),
            models.CheckConstraint(
                condition=models.Q(default_unit_price__gte=0),
                name='service_default_price_nonnegative',
            ),
        ]
        indexes = [
            models.Index(fields=['property', 'is_active']),
            models.Index(fields=['charge_method']),
        ]

    def __str__(self):
        return f'{self.property} - {self.service_code}'


class Meter(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='meters')
    service_definition = models.ForeignKey(
        ServiceDefinition,
        on_delete=models.PROTECT,
        related_name='meters',
    )
    meter_code = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, blank=True)
    initial_value = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(0)],
    )
    installed_on = models.DateField(blank=True, null=True)
    retired_on = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dong_ho'
        ordering = ['room', 'meter_code']
        verbose_name = 'Meter'
        verbose_name_plural = 'Meters'
        constraints = [
            models.UniqueConstraint(fields=['room', 'meter_code'], name='unique_meter_code_per_room'),
            models.CheckConstraint(
                condition=models.Q(initial_value__gte=0),
                name='meter_initial_value_nonnegative',
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(retired_on__isnull=True)
                    | models.Q(installed_on__isnull=True)
                    | models.Q(retired_on__gte=models.F('installed_on'))
                ),
                name='meter_retired_on_not_before_installed',
            ),
        ]
        indexes = [
            models.Index(fields=['room', 'is_active']),
            models.Index(fields=['service_definition']),
            models.Index(fields=['serial_number']),
        ]

    def __str__(self):
        return f'{self.room} - {self.meter_code}'

    def clean(self):
        super().clean()
        errors = {}
        if self.room_id and self.service_definition_id:
            if self.service_definition.property_id != self.room.property_id:
                errors['service_definition'] = 'Meter service must belong to the Room Property.'
            if self.service_definition.charge_method != ServiceDefinition.CHARGE_USAGE:
                errors['service_definition'] = 'Meter service must use the usage-based charge method.'
        if self.installed_on and self.retired_on and self.retired_on < self.installed_on:
            errors['retired_on'] = 'Retired date must be on or after installed date.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.PROTECT, related_name='readings')
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    previous_value = models.DecimalField(max_digits=14, decimal_places=3, validators=[MinValueValidator(0)])
    current_value = models.DecimalField(max_digits=14, decimal_places=3, validators=[MinValueValidator(0)])
    consumption = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=Decimal('0.000'),
        editable=False,
        validators=[MinValueValidator(0)],
    )
    read_at = models.DateTimeField(default=timezone.now)
    captured_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='captured_meter_readings',
        blank=True,
        null=True,
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chi_so_dong_ho'
        ordering = ['-year', '-month', 'meter']
        verbose_name = 'Meter Reading'
        verbose_name_plural = 'Meter Readings'
        constraints = [
            models.UniqueConstraint(fields=['meter', 'month', 'year'], name='unique_meter_reading_period'),
            models.CheckConstraint(
                condition=models.Q(month__gte=1) & models.Q(month__lte=12),
                name='meter_reading_month_valid',
            ),
            models.CheckConstraint(condition=models.Q(year__gte=2000), name='meter_reading_year_valid'),
            models.CheckConstraint(
                condition=models.Q(previous_value__gte=0),
                name='meter_reading_previous_nonnegative',
            ),
            models.CheckConstraint(
                condition=models.Q(current_value__gte=models.F('previous_value')),
                name='meter_reading_current_not_decreasing',
            ),
            models.CheckConstraint(
                condition=models.Q(consumption__gte=0),
                name='meter_reading_consumption_nonnegative',
            ),
        ]
        indexes = [
            models.Index(fields=['year', 'month']),
            models.Index(fields=['read_at']),
            models.Index(fields=['captured_by']),
        ]

    def __str__(self):
        return f'{self.meter} - {self.month:02d}/{self.year}'

    def clean(self):
        super().clean()
        if self.current_value < self.previous_value:
            raise ValidationError({'current_value': 'Current reading must be greater than or equal to previous reading.'})
        self.consumption = self.current_value - self.previous_value

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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

    def recalculate_totals(self, commit=True, require_current_total_match=True):
        detail = getattr(self, 'detail', None)
        if detail is None:
            total = self.total_amount
        else:
            from .services import validated_compatibility_line_total

            total = validated_compatibility_line_total(self, detail=detail)
            if require_current_total_match and total != self.total_amount:
                raise ValidationError('Invoice line total does not match the stored invoice total.')

        paid = self.payments.aggregate(total=Sum('amount'))['total'] or MONEY_ZERO
        if paid > total:
            raise ValidationError('Invoice payments cannot exceed the validated invoice line total.')
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
        if kwargs.get('update_fields') is not None:
            raise ValueError('InvoiceDetail partial saves are not supported; save the complete snapshot instead.')
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)

            from .services import synchronize_compatibility_lines

            line_total = synchronize_compatibility_lines(self)
            self.invoice.recalculate_totals(require_current_total_match=False)
            if line_total != self.invoice.total_amount:
                raise ValidationError('Invoice compatibility-line total does not match the invoice total.')


class InvoiceLine(models.Model):
    TYPE_RENT = 'rent'
    TYPE_ELECTRICITY = 'electricity'
    TYPE_WATER = 'water'
    TYPE_SERVICE = 'service'
    TYPE_ADJUSTMENT = 'adjustment'
    TYPE_DISCOUNT = 'discount'

    LINE_TYPE_CHOICES = (
        (TYPE_RENT, 'Rent'),
        (TYPE_ELECTRICITY, 'Electricity'),
        (TYPE_WATER, 'Water'),
        (TYPE_SERVICE, 'Service'),
        (TYPE_ADJUSTMENT, 'Adjustment'),
        (TYPE_DISCOUNT, 'Discount'),
    )

    DIRECTION_CHARGE = 'charge'
    DIRECTION_CREDIT = 'credit'

    DIRECTION_CHOICES = (
        (DIRECTION_CHARGE, 'Charge'),
        (DIRECTION_CREDIT, 'Credit'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    line_code = models.CharField(max_length=50)
    line_type = models.CharField(max_length=20, choices=LINE_TYPE_CHOICES)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default=DIRECTION_CHARGE)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=Decimal('1.000'),
        validators=[MinValueValidator(0)],
    )
    unit = models.CharField(max_length=30, blank=True)
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=MONEY_ZERO,
        validators=[MinValueValidator(0)],
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=MONEY_ZERO,
        validators=[MinValueValidator(0)],
    )
    sort_order = models.PositiveIntegerField(default=0)
    service_definition = models.ForeignKey(
        ServiceDefinition,
        on_delete=models.PROTECT,
        related_name='invoice_lines',
        blank=True,
        null=True,
    )
    meter_reading = models.ForeignKey(
        MeterReading,
        on_delete=models.PROTECT,
        related_name='invoice_lines',
        blank=True,
        null=True,
    )
    legacy_detail = models.ForeignKey(
        InvoiceDetail,
        on_delete=models.PROTECT,
        related_name='compatibility_lines',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dong_hoa_don'
        ordering = ['invoice', 'sort_order', 'pk']
        verbose_name = 'Invoice Line'
        verbose_name_plural = 'Invoice Lines'
        constraints = [
            models.UniqueConstraint(fields=['invoice', 'line_code'], name='unique_line_code_per_invoice'),
            models.CheckConstraint(condition=models.Q(quantity__gte=0), name='invoice_line_quantity_nonnegative'),
            models.CheckConstraint(condition=models.Q(unit_price__gte=0), name='invoice_line_unit_price_nonnegative'),
            models.CheckConstraint(condition=models.Q(amount__gte=0), name='invoice_line_amount_nonnegative'),
        ]
        indexes = [
            models.Index(fields=['invoice', 'sort_order']),
            models.Index(fields=['line_type']),
            models.Index(fields=['service_definition']),
            models.Index(fields=['meter_reading']),
        ]

    def __str__(self):
        return f'{self.invoice} - {self.line_code}'

    @property
    def signed_amount(self):
        if self.direction == self.DIRECTION_CREDIT:
            return -self.amount
        return self.amount

    def clean(self):
        super().clean()
        errors = {}
        if self.invoice_id:
            invoice_room = self.invoice.contract.room
            if self.service_definition_id and self.service_definition.property_id != invoice_room.property_id:
                errors['service_definition'] = 'Invoice line service must belong to the invoiced Room Property.'
            if self.meter_reading_id:
                meter = self.meter_reading.meter
                if meter.room_id != invoice_room.pk:
                    errors['meter_reading'] = 'Meter reading must belong to the invoiced Room.'
                if self.service_definition_id and meter.service_definition_id != self.service_definition_id:
                    errors['service_definition'] = 'Invoice line service must match the Meter Reading service.'
            if self.legacy_detail_id and self.legacy_detail.invoice_id != self.invoice_id:
                errors['legacy_detail'] = 'Legacy detail must belong to the same Invoice.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)
            self.invoice.recalculate_totals()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            invoice = self.invoice
            result = super().delete(*args, **kwargs)
            invoice.recalculate_totals()
            return result
