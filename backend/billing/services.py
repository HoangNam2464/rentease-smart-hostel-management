from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Invoice, InvoiceDetail, InvoiceLine, PaymentHistory, PriceConfig


COMPATIBILITY_LINE_SPECS = (
    {
        'line_code': 'legacy-rent',
        'line_type': InvoiceLine.TYPE_RENT,
        'description': 'Legacy rent snapshot',
        'unit': 'month',
        'sort_order': 10,
    },
    {
        'line_code': 'legacy-electricity',
        'line_type': InvoiceLine.TYPE_ELECTRICITY,
        'description': 'Legacy electricity snapshot',
        'unit': 'kWh',
        'sort_order': 20,
    },
    {
        'line_code': 'legacy-water',
        'line_type': InvoiceLine.TYPE_WATER,
        'description': 'Legacy water snapshot',
        'unit': 'm3',
        'sort_order': 30,
    },
    {
        'line_code': 'legacy-service',
        'line_type': InvoiceLine.TYPE_SERVICE,
        'description': 'Legacy service snapshot',
        'unit': 'month',
        'sort_order': 40,
    },
)
COMPATIBILITY_LINE_CODES = tuple(spec['line_code'] for spec in COMPATIBILITY_LINE_SPECS)


def _compatibility_line_values(detail):
    return {
        'legacy-rent': {
            'quantity': Decimal('1.000'),
            'unit_price': detail.rent_amount,
            'amount': detail.rent_amount,
        },
        'legacy-electricity': {
            'quantity': Decimal(detail.electricity_end - detail.electricity_start),
            'unit_price': detail.electricity_unit_price,
            'amount': detail.electricity_amount,
        },
        'legacy-water': {
            'quantity': Decimal(detail.water_end - detail.water_start),
            'unit_price': detail.water_unit_price,
            'amount': detail.water_amount,
        },
        'legacy-service': {
            'quantity': Decimal('1.000'),
            'unit_price': detail.service_amount,
            'amount': detail.service_amount,
        },
    }


@transaction.atomic
def synchronize_compatibility_lines(detail):
    if not detail.pk or not detail.invoice_id:
        raise ValidationError('InvoiceDetail must be saved before compatibility lines can be synchronized.')

    existing_lines = list(
        InvoiceLine.objects.select_for_update()
        .filter(invoice_id=detail.invoice_id, line_code__in=COMPATIBILITY_LINE_CODES)
        .order_by('line_code')
    )
    conflict = next(
        (line for line in existing_lines if line.legacy_detail_id != detail.pk),
        None,
    )
    if conflict is not None:
        raise ValidationError({
            'invoice': (
                f'Reserved compatibility line {conflict.line_code} is not owned by '
                'this InvoiceDetail.'
            ),
        })

    values_by_code = _compatibility_line_values(detail)
    for spec in COMPATIBILITY_LINE_SPECS:
        values = values_by_code[spec['line_code']]
        InvoiceLine.objects.update_or_create(
            invoice_id=detail.invoice_id,
            line_code=spec['line_code'],
            defaults={
                'line_type': spec['line_type'],
                'direction': InvoiceLine.DIRECTION_CHARGE,
                'description': spec['description'],
                'quantity': values['quantity'],
                'unit': spec['unit'],
                'unit_price': values['unit_price'],
                'amount': values['amount'],
                'sort_order': spec['sort_order'],
                'service_definition': None,
                'meter_reading': None,
                'legacy_detail': detail,
            },
        )

    synchronized_lines = list(
        InvoiceLine.objects.filter(
            invoice_id=detail.invoice_id,
            line_code__in=COMPATIBILITY_LINE_CODES,
        ).order_by('sort_order')
    )
    if len(synchronized_lines) != len(COMPATIBILITY_LINE_SPECS):
        raise ValidationError('InvoiceDetail compatibility-line count is not exactly four.')
    if any(line.legacy_detail_id != detail.pk for line in synchronized_lines):
        raise ValidationError('InvoiceDetail compatibility-line ownership is inconsistent.')

    line_total = sum((line.signed_amount for line in synchronized_lines), Decimal('0.00'))
    if line_total != detail.total_line_amount:
        raise ValidationError('InvoiceDetail compatibility-line total does not match its snapshot total.')
    return line_total


@transaction.atomic
def generate_invoice(
    *,
    contract,
    month,
    year,
    electricity_start,
    electricity_end,
    water_start,
    water_end,
    due_date=None,
    issued_date=None,
    note='',
):
    if not PriceConfig.objects.filter(room=contract.room, month=month, year=year).exists():
        raise ValidationError('Price config is required before generating an invoice.')

    invoice = Invoice(
        contract=contract,
        month=month,
        year=year,
        issued_date=issued_date or timezone.localdate(),
        due_date=due_date,
        note=note,
    )
    invoice.full_clean()
    invoice.save()
    InvoiceDetail.objects.create(
        invoice=invoice,
        electricity_start=electricity_start,
        electricity_end=electricity_end,
        water_start=water_start,
        water_end=water_end,
    )
    invoice.refresh_from_db()
    return invoice


def recalculate_invoice(invoice):
    invoice.recalculate_totals()
    invoice.refresh_from_db()
    return invoice


@transaction.atomic
def record_payment(*, invoice, amount, method, collector=None, transaction_code='', note='', paid_at=None):
    payment = PaymentHistory.objects.create(
        invoice=invoice,
        amount=amount,
        method=method,
        collector=collector,
        transaction_code=transaction_code,
        note=note,
        paid_at=paid_at or timezone.now(),
    )
    invoice.refresh_from_db()
    return payment


def mark_overdue_invoices():
    today = timezone.localdate()
    invoices = Invoice.objects.filter(
        due_date__lt=today,
        remaining_amount__gt=0,
    ).exclude(status=Invoice.STATUS_PAID)
    return invoices.update(status=Invoice.STATUS_OVERDUE)
