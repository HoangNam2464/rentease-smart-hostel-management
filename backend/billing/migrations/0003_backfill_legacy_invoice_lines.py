from decimal import Decimal

from django.db import migrations
from django.db.models import Count, Sum


MONEY_ZERO = Decimal('0.00')
ONE_ITEM = Decimal('1.000')
COMPATIBILITY_CODES = (
    'legacy-rent',
    'legacy-electricity',
    'legacy-water',
    'legacy-service',
)


def validate_source_detail(detail):
    invoice = detail.invoice
    electricity_usage = detail.electricity_end - detail.electricity_start
    water_usage = detail.water_end - detail.water_start

    if electricity_usage < 0 or water_usage < 0:
        raise RuntimeError(
            f'InvoiceDetail {detail.pk} has decreasing utility readings; '
            'compatibility-line backfill cannot continue.'
        )

    snapshot_amounts = (
        detail.rent_amount,
        detail.electricity_amount,
        detail.water_amount,
        detail.service_amount,
    )
    if any(amount < MONEY_ZERO for amount in snapshot_amounts):
        raise RuntimeError(
            f'InvoiceDetail {detail.pk} has a negative snapshot amount; '
            'compatibility-line backfill cannot continue.'
        )

    expected_electricity = Decimal(electricity_usage) * detail.electricity_unit_price
    expected_water = Decimal(water_usage) * detail.water_unit_price
    if detail.electricity_amount != expected_electricity:
        raise RuntimeError(
            f'InvoiceDetail {detail.pk} electricity snapshot does not match usage and unit price.'
        )
    if detail.water_amount != expected_water:
        raise RuntimeError(
            f'InvoiceDetail {detail.pk} water snapshot does not match usage and unit price.'
        )

    detail_total = sum(snapshot_amounts, MONEY_ZERO)
    if detail_total != invoice.total_amount:
        raise RuntimeError(
            f'Invoice {invoice.pk} total {invoice.total_amount} does not match '
            f'InvoiceDetail {detail.pk} snapshot total {detail_total}.'
        )


def build_compatibility_lines(InvoiceLine, detail):
    invoice_id = detail.invoice_id
    return [
        InvoiceLine(
            invoice_id=invoice_id,
            line_code='legacy-rent',
            line_type='rent',
            direction='charge',
            description='Legacy rent snapshot',
            quantity=ONE_ITEM,
            unit='month',
            unit_price=detail.rent_amount,
            amount=detail.rent_amount,
            sort_order=10,
            legacy_detail_id=detail.pk,
        ),
        InvoiceLine(
            invoice_id=invoice_id,
            line_code='legacy-electricity',
            line_type='electricity',
            direction='charge',
            description='Legacy electricity snapshot',
            quantity=Decimal(detail.electricity_end - detail.electricity_start),
            unit='kWh',
            unit_price=detail.electricity_unit_price,
            amount=detail.electricity_amount,
            sort_order=20,
            legacy_detail_id=detail.pk,
        ),
        InvoiceLine(
            invoice_id=invoice_id,
            line_code='legacy-water',
            line_type='water',
            direction='charge',
            description='Legacy water snapshot',
            quantity=Decimal(detail.water_end - detail.water_start),
            unit='m3',
            unit_price=detail.water_unit_price,
            amount=detail.water_amount,
            sort_order=30,
            legacy_detail_id=detail.pk,
        ),
        InvoiceLine(
            invoice_id=invoice_id,
            line_code='legacy-service',
            line_type='service',
            direction='charge',
            description='Legacy service snapshot',
            quantity=ONE_ITEM,
            unit='month',
            unit_price=detail.service_amount,
            amount=detail.service_amount,
            sort_order=40,
            legacy_detail_id=detail.pk,
        ),
    ]


def backfill_legacy_invoice_lines(apps, schema_editor):
    InvoiceDetail = apps.get_model('billing', 'InvoiceDetail')
    InvoiceLine = apps.get_model('billing', 'InvoiceLine')
    alias = schema_editor.connection.alias

    details = InvoiceDetail.objects.using(alias).select_related('invoice').order_by('pk')
    collision = (
        InvoiceLine.objects.using(alias)
        .filter(invoice__detail__isnull=False, line_code__in=COMPATIBILITY_CODES)
        .values('invoice_id', 'line_code')
        .order_by('invoice_id', 'line_code')
        .first()
    )
    if collision is not None:
        raise RuntimeError(
            f"Invoice {collision['invoice_id']} already has reserved compatibility line "
            f"{collision['line_code']}; backfill cannot continue."
        )

    for detail in details.iterator(chunk_size=500):
        validate_source_detail(detail)

    pending_lines = []
    for detail in details.iterator(chunk_size=500):
        pending_lines.extend(build_compatibility_lines(InvoiceLine, detail))
        if len(pending_lines) >= 1000:
            InvoiceLine.objects.using(alias).bulk_create(pending_lines, batch_size=1000)
            pending_lines = []
    if pending_lines:
        InvoiceLine.objects.using(alias).bulk_create(pending_lines, batch_size=1000)

    reconciliation = {
        row['legacy_detail_id']: (row['line_count'], row['line_total'])
        for row in (
            InvoiceLine.objects.using(alias)
            .filter(
                legacy_detail_id__isnull=False,
                line_code__in=COMPATIBILITY_CODES,
                direction='charge',
            )
            .values('legacy_detail_id')
            .annotate(line_count=Count('pk'), line_total=Sum('amount'))
        )
    }
    for detail in details.iterator(chunk_size=500):
        detail_total = (
            detail.rent_amount
            + detail.electricity_amount
            + detail.water_amount
            + detail.service_amount
        )
        line_count, line_total = reconciliation.get(detail.pk, (0, None))
        if line_count != 4 or line_total != detail_total or line_total != detail.invoice.total_amount:
            raise RuntimeError(
                f'InvoiceDetail {detail.pk} compatibility lines failed exact reconciliation.'
            )


def reverse_legacy_invoice_lines(apps, schema_editor):
    InvoiceLine = apps.get_model('billing', 'InvoiceLine')
    InvoiceLine.objects.using(schema_editor.connection.alias).filter(
        legacy_detail_id__isnull=False,
        line_code__in=COMPATIBILITY_CODES,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_add_billing_meter_foundations'),
    ]

    operations = [
        migrations.RunPython(backfill_legacy_invoice_lines, reverse_legacy_invoice_lines),
    ]
