from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Invoice, InvoiceDetail, PaymentHistory, PriceConfig


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
