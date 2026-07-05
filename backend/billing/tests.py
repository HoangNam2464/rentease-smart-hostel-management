from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase

from accounts.models import UserProfile
from contracts.models import Contract
from properties.models import Property, Room
from tenants.models import Tenant

from .models import (
    Invoice,
    InvoiceDetail,
    InvoiceLine,
    Meter,
    MeterReading,
    PaymentHistory,
    PriceConfig,
    ServiceDefinition,
)
from .services import generate_invoice, record_payment, validated_compatibility_line_total


class BillingInvariantTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner_user = get_user_model().objects.create_user(
            username="billing_invariant_owner",
            password="local-test-password",
            user_type="OWNER",
        )
        cls.owner = UserProfile.objects.create(user=cls.owner_user, full_name="Billing Owner")
        cls.property_record = Property.objects.create(
            owner=cls.owner,
            property_code="BILLING-PROPERTY",
            name="Billing Property",
        )
        cls.room = Room.objects.create(
            owner=cls.owner,
            property=cls.property_record,
            room_code="BILLING-ROOM",
            room_name="Billing Room",
            default_rent=Decimal("5000000.00"),
        )
        tenant = Tenant.objects.create(
            full_name="Billing Tenant",
            citizen_id="BILLING-INVARIANT",
        )
        cls.contract = Contract.objects.create(
            room=cls.room,
            tenant=tenant,
            contract_code="BILLING-CONTRACT",
            signed_date=date(2026, 1, 1),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            rent_amount=Decimal("5000000.00"),
            deposit_amount=Decimal("5000000.00"),
            status="active",
        )
        cls.price_config = PriceConfig.objects.create(
            room=cls.room,
            month=6,
            year=2026,
            electricity_unit_price=Decimal("3500.00"),
            water_unit_price=Decimal("15000.00"),
            service_fee=Decimal("150000.00"),
            effective_from=date(2026, 6, 1),
        )

    def create_invoice(self):
        return Invoice.objects.create(
            contract=self.contract,
            month=6,
            year=2026,
            issued_date=date(2026, 6, 1),
        )

    def test_invoice_detail_snapshots_prices_and_recalculates_total(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )

        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_unit_price, Decimal("3500.00"))
        self.assertEqual(detail.water_unit_price, Decimal("15000.00"))
        self.assertEqual(detail.electricity_amount, Decimal("35000.00"))
        self.assertEqual(detail.water_amount, Decimal("30000.00"))
        self.assertEqual(detail.rent_amount, Decimal("5000000.00"))
        self.assertEqual(detail.service_amount, Decimal("150000.00"))
        self.assertEqual(invoice.total_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_UNPAID)
        lines = InvoiceLine.objects.filter(invoice=invoice).order_by('sort_order')
        self.assertEqual(
            list(lines.values_list('line_code', flat=True)),
            ['legacy-rent', 'legacy-electricity', 'legacy-water', 'legacy-service'],
        )
        self.assertEqual(
            sum((line.signed_amount for line in lines), Decimal('0.00')),
            invoice.total_amount,
        )
        self.assertFalse(lines.exclude(legacy_detail=detail).exists())

    def test_payment_cannot_exceed_invoice_remaining_amount(self):
        invoice = self.create_invoice()
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        PaymentHistory.objects.create(invoice=invoice, amount=Decimal("5000000.00"))

        with self.assertRaises(ValidationError):
            PaymentHistory.objects.create(invoice=invoice, amount=Decimal("216000.00"))

    def test_database_rejects_duplicate_price_config_period(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PriceConfig.objects.create(
                    room=self.room,
                    month=6,
                    year=2026,
                    electricity_unit_price=Decimal("4000.00"),
                    water_unit_price=Decimal("16000.00"),
                    service_fee=Decimal("200000.00"),
                    effective_from=date(2026, 6, 1),
                )

    def test_zero_usage_preserves_rent_and_service_total(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=100,
            water_start=20,
            water_end=20,
        )

        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_amount, Decimal("0.00"))
        self.assertEqual(detail.water_amount, Decimal("0.00"))
        self.assertEqual(detail.rent_amount, Decimal("5000000.00"))
        self.assertEqual(detail.service_amount, Decimal("150000.00"))
        self.assertEqual(invoice.total_amount, Decimal("5150000.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("5150000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_UNPAID)
        lines = InvoiceLine.objects.filter(invoice=invoice)
        self.assertEqual(lines.count(), 4)
        self.assertEqual(lines.get(line_code='legacy-electricity').quantity, Decimal('0.000'))
        self.assertEqual(lines.get(line_code='legacy-water').quantity, Decimal('0.000'))
        self.assertEqual(lines.get(line_code='legacy-electricity').amount, Decimal('0.00'))
        self.assertEqual(lines.get(line_code='legacy-water').amount, Decimal('0.00'))

    def test_invoice_detail_snapshot_changes_only_when_detail_is_resaved(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        original_snapshot = (
            detail.electricity_unit_price,
            detail.water_unit_price,
            detail.service_amount,
            detail.total_line_amount,
        )
        original_line_ids = set(InvoiceLine.objects.filter(invoice=invoice).values_list('pk', flat=True))
        original_line_amounts = dict(
            InvoiceLine.objects.filter(invoice=invoice).values_list('line_code', 'amount')
        )

        PriceConfig.objects.filter(pk=self.price_config.pk).update(
            electricity_unit_price=Decimal("9999.00"),
            water_unit_price=Decimal("88888.00"),
            service_fee=Decimal("777777.00"),
        )
        detail.refresh_from_db()
        invoice.refresh_from_db()

        self.assertEqual(
            (
                detail.electricity_unit_price,
                detail.water_unit_price,
                detail.service_amount,
                detail.total_line_amount,
            ),
            original_snapshot,
        )
        self.assertEqual(invoice.total_amount, Decimal("5215000.00"))
        self.assertEqual(
            dict(InvoiceLine.objects.filter(invoice=invoice).values_list('line_code', 'amount')),
            original_line_amounts,
        )

        detail.save()
        detail.refresh_from_db()
        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_unit_price, Decimal("9999.00"))
        self.assertEqual(detail.water_unit_price, Decimal("88888.00"))
        self.assertEqual(detail.service_amount, Decimal("777777.00"))
        self.assertEqual(invoice.total_amount, Decimal("6055543.00"))
        lines = InvoiceLine.objects.filter(invoice=invoice)
        self.assertEqual(lines.count(), 4)
        self.assertEqual(set(lines.values_list('pk', flat=True)), original_line_ids)
        self.assertEqual(lines.get(line_code='legacy-electricity').unit_price, Decimal('9999.00'))
        self.assertEqual(lines.get(line_code='legacy-water').unit_price, Decimal('88888.00'))
        self.assertEqual(lines.get(line_code='legacy-service').amount, Decimal('777777.00'))
        self.assertEqual(
            sum((line.signed_amount for line in lines), Decimal('0.00')),
            invoice.total_amount,
        )

        detail.save()
        self.assertEqual(InvoiceLine.objects.filter(invoice=invoice).count(), 4)
        self.assertEqual(
            set(InvoiceLine.objects.filter(invoice=invoice).values_list('pk', flat=True)),
            original_line_ids,
        )

    def test_invoice_detail_dual_write_conflict_rolls_back_detail_invoice_and_lines(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        InvoiceLine.objects.filter(
            invoice=invoice,
            line_code='legacy-rent',
        ).update(legacy_detail=None)
        original_lines = list(InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
            'pk',
            'line_code',
            'legacy_detail_id',
            'quantity',
            'unit_price',
            'amount',
        ))
        original_total = invoice.total_amount

        detail.electricity_end = 120
        with self.assertRaises(ValidationError):
            detail.save()

        detail.refresh_from_db()
        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_end, 110)
        self.assertEqual(detail.electricity_amount, Decimal('35000.00'))
        self.assertEqual(invoice.total_amount, original_total)
        self.assertEqual(
            list(InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
                'pk',
                'line_code',
                'legacy_detail_id',
                'quantity',
                'unit_price',
                'amount',
            )),
            original_lines,
        )

    def test_invoice_detail_rejects_partial_save_to_protect_dual_write_parity(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        original_lines = list(InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
            'pk',
            'line_code',
            'quantity',
            'unit_price',
            'amount',
        ))

        detail.electricity_end = 120
        with self.assertRaises(ValueError):
            detail.save(update_fields=['electricity_end'])

        detail.refresh_from_db()
        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_end, 110)
        self.assertEqual(invoice.total_amount, Decimal('5215000.00'))
        self.assertEqual(
            list(InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
                'pk',
                'line_code',
                'quantity',
                'unit_price',
                'amount',
            )),
            original_lines,
        )

    def test_recalculation_reads_validated_lines_and_defers_noncompatibility_lines(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        InvoiceLine.objects.create(
            invoice=invoice,
            line_code='future-adjustment',
            line_type=InvoiceLine.TYPE_ADJUSTMENT,
            direction=InvoiceLine.DIRECTION_CHARGE,
            description='Deferred adjustment',
            amount=Decimal('250000.00'),
        )
        InvoiceLine.objects.create(
            invoice=invoice,
            line_code='future-discount',
            line_type=InvoiceLine.TYPE_DISCOUNT,
            direction=InvoiceLine.DIRECTION_CREDIT,
            description='Deferred discount',
            amount=Decimal('100000.00'),
        )

        self.assertEqual(
            validated_compatibility_line_total(invoice, detail=detail),
            Decimal('5215000.00'),
        )
        invoice.recalculate_totals()
        invoice.refresh_from_db()
        self.assertEqual(invoice.total_amount, Decimal('5215000.00'))
        self.assertEqual(invoice.remaining_amount, Decimal('5215000.00'))

    def test_recalculation_fails_closed_when_a_compatibility_line_is_missing(self):
        invoice = self.create_invoice()
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        InvoiceLine.objects.filter(invoice=invoice, line_code='legacy-water').delete()

        with self.assertRaises(ValidationError):
            invoice.recalculate_totals()

        invoice.refresh_from_db()
        self.assertEqual(invoice.total_amount, Decimal('5215000.00'))
        self.assertEqual(invoice.remaining_amount, Decimal('5215000.00'))

    def test_recalculation_fails_closed_on_line_snapshot_or_header_variance(self):
        invoice = self.create_invoice()
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        InvoiceLine.objects.filter(invoice=invoice, line_code='legacy-service').update(
            amount=Decimal('150001.00'),
        )
        with self.assertRaises(ValidationError):
            invoice.recalculate_totals()

        InvoiceLine.objects.filter(invoice=invoice, line_code='legacy-service').update(
            amount=Decimal('150000.00'),
        )
        Invoice.objects.filter(pk=invoice.pk).update(total_amount=Decimal('5215001.00'))
        invoice.refresh_from_db()
        with self.assertRaises(ValidationError):
            invoice.recalculate_totals()

        invoice.refresh_from_db()
        self.assertEqual(invoice.total_amount, Decimal('5215001.00'))

    def test_payment_create_and_delete_roll_back_when_line_validation_fails(self):
        invoice = self.create_invoice()
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        InvoiceLine.objects.filter(invoice=invoice, line_code='legacy-water').delete()

        with self.assertRaises(ValidationError):
            PaymentHistory.objects.create(invoice=invoice, amount=Decimal('1000000.00'))
        self.assertFalse(PaymentHistory.objects.filter(invoice=invoice).exists())

        InvoiceDetail.objects.get(invoice=invoice).save()
        payment = PaymentHistory.objects.create(invoice=invoice, amount=Decimal('1000000.00'))
        payment_pk = payment.pk
        InvoiceLine.objects.filter(invoice=invoice, line_code='legacy-water').delete()
        with self.assertRaises(ValidationError):
            payment.delete()
        self.assertTrue(PaymentHistory.objects.filter(pk=payment_pk).exists())

    def test_detail_update_rolls_back_if_validated_line_total_would_be_overpaid(self):
        invoice = self.create_invoice()
        detail = InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        PaymentHistory.objects.create(invoice=invoice, amount=Decimal('5100000.00'))
        original_lines = list(
            InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
                'line_code', 'quantity', 'unit_price', 'amount'
            )
        )
        PriceConfig.objects.filter(pk=self.price_config.pk).update(
            electricity_unit_price=Decimal('0.00'),
            water_unit_price=Decimal('0.00'),
            service_fee=Decimal('0.00'),
        )

        with self.assertRaises(ValidationError):
            detail.save()

        detail.refresh_from_db()
        invoice.refresh_from_db()
        self.assertEqual(invoice.total_amount, Decimal('5215000.00'))
        self.assertEqual(invoice.paid_amount, Decimal('5100000.00'))
        self.assertEqual(detail.service_amount, Decimal('150000.00'))
        self.assertEqual(
            list(
                InvoiceLine.objects.filter(invoice=invoice).order_by('pk').values_list(
                    'line_code', 'quantity', 'unit_price', 'amount'
                )
            ),
            original_lines,
        )

    def test_payment_status_transitions_and_deletion_recalculate_balance(self):
        invoice = self.create_invoice()
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )

        with self.assertRaises(ValidationError):
            record_payment(
                invoice=invoice,
                amount=Decimal("0.00"),
                method=PaymentHistory.METHOD_CASH,
            )

        first_payment = record_payment(
            invoice=invoice,
            amount=Decimal("1000000.00"),
            method=PaymentHistory.METHOD_BANK_TRANSFER,
        )
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal("1000000.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("4215000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_PARTIAL)

        final_payment = record_payment(
            invoice=invoice,
            amount=Decimal("4215000.00"),
            method=PaymentHistory.METHOD_CASH,
        )
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("0.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_PAID)

        final_payment.delete()
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal("1000000.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("4215000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_PARTIAL)

        first_payment.delete()
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal("0.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_UNPAID)
        self.assertEqual(InvoiceLine.objects.filter(invoice=invoice).count(), 4)
        self.assertEqual(
            sum(
                (line.signed_amount for line in InvoiceLine.objects.filter(invoice=invoice)),
                Decimal('0.00'),
            ),
            invoice.total_amount,
        )

    def test_invoice_detail_rejects_decreasing_meter_readings(self):
        invoice = self.create_invoice()

        with self.assertRaises(ValidationError):
            InvoiceDetail.objects.create(
                invoice=invoice,
                electricity_start=110,
                electricity_end=100,
                water_start=20,
                water_end=22,
            )
        with self.assertRaises(ValidationError):
            InvoiceDetail.objects.create(
                invoice=invoice,
                electricity_start=100,
                electricity_end=110,
                water_start=22,
                water_end=20,
            )

        self.assertFalse(InvoiceDetail.objects.filter(invoice=invoice).exists())

    def test_past_due_unpaid_invoice_recalculates_to_overdue(self):
        invoice = Invoice.objects.create(
            contract=self.contract,
            month=6,
            year=2026,
            issued_date=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
        )
        InvoiceDetail.objects.create(
            invoice=invoice,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )

        invoice.refresh_from_db()
        self.assertEqual(invoice.status, Invoice.STATUS_OVERDUE)
        self.assertEqual(invoice.remaining_amount, invoice.total_amount)

    def test_generate_invoice_is_atomic_and_requires_price_config(self):
        with self.assertRaises(ValidationError):
            generate_invoice(
                contract=self.contract,
                month=7,
                year=2026,
                electricity_start=110,
                electricity_end=120,
                water_start=22,
                water_end=24,
            )
        self.assertFalse(Invoice.objects.filter(contract=self.contract, month=7, year=2026).exists())

        invoice = generate_invoice(
            contract=self.contract,
            month=6,
            year=2026,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
        )
        self.assertEqual(invoice.total_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.paid_amount, Decimal("0.00"))
        self.assertEqual(invoice.remaining_amount, Decimal("5215000.00"))
        self.assertEqual(invoice.status, Invoice.STATUS_UNPAID)

        with self.assertRaises(ValidationError):
            generate_invoice(
                contract=self.contract,
                month=6,
                year=2026,
                electricity_start=100,
                electricity_end=110,
                water_start=20,
                water_end=22,
            )
        self.assertEqual(Invoice.objects.filter(contract=self.contract, month=6, year=2026).count(), 1)


class AdditiveBillingFoundationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner_user = get_user_model().objects.create_user(
            username='billing_foundation_owner',
            password='local-test-password',
            user_type='OWNER',
        )
        cls.owner = UserProfile.objects.create(user=cls.owner_user, full_name='Billing Foundation Owner')
        cls.property_record = Property.objects.create(
            owner=cls.owner,
            property_code='BILLING-FOUNDATION-PROPERTY',
            name='Billing Foundation Property',
        )
        cls.room = Room.objects.create(
            owner=cls.owner,
            property=cls.property_record,
            room_code='BILLING-FOUNDATION-ROOM',
            room_name='Billing Foundation Room',
            default_rent=Decimal('5000000.00'),
        )
        tenant = Tenant.objects.create(
            full_name='Billing Foundation Tenant',
            citizen_id='BILLING-FOUNDATION',
        )
        cls.contract = Contract.objects.create(
            room=cls.room,
            tenant=tenant,
            contract_code='BILLING-FOUNDATION-CONTRACT',
            signed_date=date(2026, 1, 1),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            rent_amount=Decimal('5000000.00'),
            deposit_amount=Decimal('5000000.00'),
            status='active',
        )
        cls.electricity_service = ServiceDefinition.objects.create(
            property=cls.property_record,
            service_code='ELECTRICITY',
            name='Electricity',
            charge_method=ServiceDefinition.CHARGE_USAGE,
            unit='kWh',
            default_unit_price=Decimal('3500.00'),
        )
        cls.meter = Meter.objects.create(
            room=cls.room,
            service_definition=cls.electricity_service,
            meter_code='ELECTRICITY-METER',
            serial_number='SERIAL-001',
            initial_value=Decimal('100.000'),
            installed_on=date(2026, 1, 1),
        )

    def create_invoice(self):
        return Invoice.objects.create(
            contract=self.contract,
            month=6,
            year=2026,
            issued_date=date(2026, 6, 1),
        )

    def test_service_code_is_unique_per_property(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ServiceDefinition.objects.create(
                    property=self.property_record,
                    service_code='ELECTRICITY',
                    name='Duplicate electricity',
                    charge_method=ServiceDefinition.CHARGE_USAGE,
                    unit='kWh',
                    default_unit_price=Decimal('4000.00'),
                )

    def test_meter_rejects_fixed_service_and_cross_property_service(self):
        fixed_service = ServiceDefinition.objects.create(
            property=self.property_record,
            service_code='INTERNET',
            name='Internet',
            charge_method=ServiceDefinition.CHARGE_FIXED,
            unit='month',
            default_unit_price=Decimal('100000.00'),
        )
        with self.assertRaises(ValidationError):
            Meter.objects.create(
                room=self.room,
                service_definition=fixed_service,
                meter_code='INVALID-FIXED-METER',
            )

        other_user = get_user_model().objects.create_user(username='other_meter_owner', user_type='OWNER')
        other_owner = UserProfile.objects.create(user=other_user, full_name='Other Meter Owner')
        other_property = Property.objects.create(
            owner=other_owner,
            property_code='OTHER-METER-PROPERTY',
            name='Other Meter Property',
        )
        other_service = ServiceDefinition.objects.create(
            property=other_property,
            service_code='ELECTRICITY',
            name='Other electricity',
            charge_method=ServiceDefinition.CHARGE_USAGE,
            unit='kWh',
            default_unit_price=Decimal('3500.00'),
        )
        with self.assertRaises(ValidationError):
            Meter.objects.create(
                room=self.room,
                service_definition=other_service,
                meter_code='INVALID-CROSS-PROPERTY',
            )

    def test_meter_code_is_unique_per_room_and_dates_are_ordered(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Meter.objects.bulk_create([
                    Meter(
                        room=self.room,
                        service_definition=self.electricity_service,
                        meter_code='ELECTRICITY-METER',
                    ),
                ])

        with self.assertRaises(ValidationError):
            Meter.objects.create(
                room=self.room,
                service_definition=self.electricity_service,
                meter_code='INVALID-DATES',
                installed_on=date(2026, 6, 2),
                retired_on=date(2026, 6, 1),
            )

    def test_meter_reading_snapshots_consumption_and_period_is_unique(self):
        reading = MeterReading.objects.create(
            meter=self.meter,
            month=6,
            year=2026,
            previous_value=Decimal('100.000'),
            current_value=Decimal('112.500'),
            captured_by=self.owner_user,
        )
        self.assertEqual(reading.consumption, Decimal('12.500'))

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MeterReading.objects.bulk_create([
                    MeterReading(
                        meter=self.meter,
                        month=6,
                        year=2026,
                        previous_value=Decimal('112.500'),
                        current_value=Decimal('120.000'),
                        consumption=Decimal('7.500'),
                    ),
                ])

    def test_meter_reading_rejects_decreasing_value(self):
        with self.assertRaises(ValidationError):
            MeterReading.objects.create(
                meter=self.meter,
                month=6,
                year=2026,
                previous_value=Decimal('120.000'),
                current_value=Decimal('119.999'),
            )

    def test_invoice_line_signed_amount_and_unique_code_do_not_change_invoice_total(self):
        invoice = self.create_invoice()
        line = InvoiceLine.objects.create(
            invoice=invoice,
            line_code='RENT',
            line_type=InvoiceLine.TYPE_RENT,
            direction=InvoiceLine.DIRECTION_CHARGE,
            description='Rent snapshot',
            quantity=Decimal('1.000'),
            unit='month',
            unit_price=Decimal('5000000.00'),
            amount=Decimal('5000000.00'),
        )
        credit = InvoiceLine.objects.create(
            invoice=invoice,
            line_code='DISCOUNT',
            line_type=InvoiceLine.TYPE_DISCOUNT,
            direction=InvoiceLine.DIRECTION_CREDIT,
            description='Discount snapshot',
            quantity=Decimal('1.000'),
            unit='item',
            unit_price=Decimal('100000.00'),
            amount=Decimal('100000.00'),
        )
        invoice.refresh_from_db()
        self.assertEqual(line.signed_amount, Decimal('5000000.00'))
        self.assertEqual(credit.signed_amount, Decimal('-100000.00'))
        self.assertEqual(invoice.total_amount, Decimal('0.00'))

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                InvoiceLine.objects.bulk_create([
                    InvoiceLine(
                        invoice=invoice,
                        line_code='RENT',
                        line_type=InvoiceLine.TYPE_RENT,
                        description='Duplicate rent',
                    ),
                ])

    def test_invoice_line_rejects_cross_room_sources(self):
        invoice = self.create_invoice()
        other_room = Room.objects.create(
            owner=self.owner,
            property=self.property_record,
            room_code='OTHER-BILLING-ROOM',
            room_name='Other Billing Room',
            default_rent=Decimal('4000000.00'),
        )
        other_meter = Meter.objects.create(
            room=other_room,
            service_definition=self.electricity_service,
            meter_code='OTHER-ELECTRICITY-METER',
        )
        other_reading = MeterReading.objects.create(
            meter=other_meter,
            month=6,
            year=2026,
            previous_value=Decimal('0.000'),
            current_value=Decimal('10.000'),
        )

        with self.assertRaises(ValidationError):
            InvoiceLine.objects.create(
                invoice=invoice,
                line_code='WRONG-METER',
                line_type=InvoiceLine.TYPE_ELECTRICITY,
                description='Wrong meter source',
                meter_reading=other_reading,
            )


class AdditiveBillingMigrationTests(TransactionTestCase):
    migrate_from = ('billing', '0001_initial')
    migrate_to = ('billing', '0002_add_billing_meter_foundations')

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        targets = [target, ('properties', '0004_require_room_property_and_scope_room_code')]
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_existing_invoice_survives_forward_and_backward_migration(self):
        old_apps = self.migrate(self.migrate_from)
        User = old_apps.get_model('accounts', 'User')
        UserProfileModel = old_apps.get_model('accounts', 'UserProfile')
        PropertyModel = old_apps.get_model('properties', 'Property')
        RoomModel = old_apps.get_model('properties', 'Room')
        TenantModel = old_apps.get_model('tenants', 'Tenant')
        ContractModel = old_apps.get_model('contracts', 'Contract')
        InvoiceModel = old_apps.get_model('billing', 'Invoice')

        user = User.objects.create(username='billing_migration_owner', user_type='OWNER')
        owner = UserProfileModel.objects.create(user=user, full_name='Billing Migration Owner')
        property_record = PropertyModel.objects.create(
            owner=owner,
            property_code='BILLING-MIGRATION-PROPERTY',
            name='Billing Migration Property',
        )
        room = RoomModel.objects.create(
            owner=owner,
            property=property_record,
            room_code='BILLING-MIGRATION-ROOM',
            room_name='Billing Migration Room',
            default_rent=Decimal('3000000.00'),
        )
        tenant = TenantModel.objects.create(full_name='Billing Migration Tenant', citizen_id='BILLING-MIGRATION')
        contract = ContractModel.objects.create(
            room=room,
            tenant=tenant,
            contract_code='BILLING-MIGRATION-CONTRACT',
            signed_date=date(2026, 1, 1),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            rent_amount=Decimal('3000000.00'),
            deposit_amount=Decimal('3000000.00'),
            status='active',
        )
        invoice = InvoiceModel.objects.create(
            contract=contract,
            invoice_code='INV-MIGRATION',
            month=6,
            year=2026,
            issued_date=date(2026, 6, 1),
        )

        new_apps = self.migrate(self.migrate_to)
        NewInvoice = new_apps.get_model('billing', 'Invoice')
        for model_name in ('ServiceDefinition', 'Meter', 'MeterReading', 'InvoiceLine'):
            self.assertIsNotNone(new_apps.get_model('billing', model_name))
        self.assertTrue(NewInvoice.objects.filter(pk=invoice.pk, invoice_code='INV-MIGRATION').exists())

        reversed_apps = self.migrate(self.migrate_from)
        ReversedInvoice = reversed_apps.get_model('billing', 'Invoice')
        self.assertTrue(ReversedInvoice.objects.filter(pk=invoice.pk, invoice_code='INV-MIGRATION').exists())


class InvoiceLineBackfillMigrationTests(TransactionTestCase):
    migrate_from = ('billing', '0002_add_billing_meter_foundations')
    migrate_to = ('billing', '0003_backfill_legacy_invoice_lines')
    compatibility_codes = {
        'legacy-rent',
        'legacy-electricity',
        'legacy-water',
        'legacy-service',
    }

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        targets = [target, ('properties', '0004_require_room_property_and_scope_room_code')]
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def create_foundation(self, apps):
        User = apps.get_model('accounts', 'User')
        UserProfileModel = apps.get_model('accounts', 'UserProfile')
        PropertyModel = apps.get_model('properties', 'Property')
        RoomModel = apps.get_model('properties', 'Room')
        TenantModel = apps.get_model('tenants', 'Tenant')
        ContractModel = apps.get_model('contracts', 'Contract')

        user = User.objects.create(username='line_backfill_owner', user_type='OWNER')
        owner = UserProfileModel.objects.create(user=user, full_name='Line Backfill Owner')
        property_record = PropertyModel.objects.create(
            owner=owner,
            property_code='LINE-BACKFILL-PROPERTY',
            name='Line Backfill Property',
        )
        room = RoomModel.objects.create(
            owner=owner,
            property=property_record,
            room_code='LINE-BACKFILL-ROOM',
            room_name='Line Backfill Room',
            default_rent=Decimal('5000000.00'),
        )
        tenant = TenantModel.objects.create(
            full_name='Line Backfill Tenant',
            citizen_id='LINE-BACKFILL-TENANT',
        )
        contract = ContractModel.objects.create(
            room=room,
            tenant=tenant,
            contract_code='LINE-BACKFILL-CONTRACT',
            signed_date=date(2026, 1, 1),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            rent_amount=Decimal('5000000.00'),
            deposit_amount=Decimal('5000000.00'),
            status='active',
        )
        return contract

    def create_invoice_detail(
        self,
        apps,
        contract,
        *,
        month,
        electricity_start,
        electricity_end,
        water_start,
        water_end,
        paid_amount,
        status,
    ):
        InvoiceModel = apps.get_model('billing', 'Invoice')
        InvoiceDetailModel = apps.get_model('billing', 'InvoiceDetail')
        PaymentHistoryModel = apps.get_model('billing', 'PaymentHistory')

        electricity_unit_price = Decimal('3500.00')
        water_unit_price = Decimal('15000.00')
        rent_amount = Decimal('5000000.00')
        service_amount = Decimal('150000.00')
        electricity_amount = Decimal(electricity_end - electricity_start) * electricity_unit_price
        water_amount = Decimal(water_end - water_start) * water_unit_price
        total_amount = electricity_amount + water_amount + rent_amount + service_amount
        invoice = InvoiceModel.objects.create(
            contract=contract,
            invoice_code=f'INV-BACKFILL-{month:02d}',
            month=month,
            year=2026,
            issued_date=date(2026, month, 1),
            total_amount=total_amount,
            paid_amount=paid_amount,
            remaining_amount=total_amount - paid_amount,
            status=status,
        )
        detail = InvoiceDetailModel.objects.create(
            invoice=invoice,
            electricity_start=electricity_start,
            electricity_end=electricity_end,
            electricity_unit_price=electricity_unit_price,
            electricity_amount=electricity_amount,
            water_start=water_start,
            water_end=water_end,
            water_unit_price=water_unit_price,
            water_amount=water_amount,
            rent_amount=rent_amount,
            service_amount=service_amount,
        )
        if paid_amount:
            PaymentHistoryModel.objects.create(
                invoice=invoice,
                amount=paid_amount,
                method='bank_transfer',
                transaction_code=f'PAY-BACKFILL-{month:02d}',
            )
        return invoice, detail

    def test_forward_and_backward_backfill_preserves_exact_financial_state(self):
        old_apps = self.migrate(self.migrate_from)
        contract = self.create_foundation(old_apps)
        InvoiceModel = old_apps.get_model('billing', 'Invoice')
        InvoiceLineModel = old_apps.get_model('billing', 'InvoiceLine')
        PaymentHistoryModel = old_apps.get_model('billing', 'PaymentHistory')

        unpaid_invoice, unpaid_detail = self.create_invoice_detail(
            old_apps,
            contract,
            month=4,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
            paid_amount=Decimal('0.00'),
            status='unpaid',
        )
        partial_invoice, partial_detail = self.create_invoice_detail(
            old_apps,
            contract,
            month=5,
            electricity_start=110,
            electricity_end=110,
            water_start=22,
            water_end=22,
            paid_amount=Decimal('1000000.00'),
            status='partial',
        )
        paid_total = Decimal('5215000.00')
        paid_invoice, paid_detail = self.create_invoice_detail(
            old_apps,
            contract,
            month=6,
            electricity_start=110,
            electricity_end=120,
            water_start=22,
            water_end=24,
            paid_amount=paid_total,
            status='paid',
        )
        header_without_detail = InvoiceModel.objects.create(
            contract=contract,
            invoice_code='INV-BACKFILL-03',
            month=3,
            year=2026,
            issued_date=date(2026, 3, 1),
        )
        invoice_snapshot = list(InvoiceModel.objects.order_by('pk').values_list(
            'pk',
            'contract_id',
            'total_amount',
            'paid_amount',
            'remaining_amount',
            'status',
        ))
        payment_snapshot = list(PaymentHistoryModel.objects.order_by('pk').values_list(
            'pk',
            'invoice_id',
            'amount',
            'method',
            'transaction_code',
        ))
        InvoiceLineModel.objects.create(
            invoice=header_without_detail,
            line_code='manual-note',
            line_type='adjustment',
            direction='charge',
            description='Unrelated line must survive reverse migration',
            quantity=Decimal('0.000'),
            unit_price=Decimal('0.00'),
            amount=Decimal('0.00'),
        )

        new_apps = self.migrate(self.migrate_to)
        NewInvoice = new_apps.get_model('billing', 'Invoice')
        NewInvoiceDetail = new_apps.get_model('billing', 'InvoiceDetail')
        NewInvoiceLine = new_apps.get_model('billing', 'InvoiceLine')
        NewPaymentHistory = new_apps.get_model('billing', 'PaymentHistory')
        ServiceDefinitionModel = new_apps.get_model('billing', 'ServiceDefinition')
        MeterModel = new_apps.get_model('billing', 'Meter')
        MeterReadingModel = new_apps.get_model('billing', 'MeterReading')

        self.assertEqual(NewInvoiceLine.objects.filter(line_code__in=self.compatibility_codes).count(), 12)
        self.assertEqual(NewInvoiceLine.objects.filter(invoice_id=header_without_detail.pk).count(), 1)
        self.assertFalse(ServiceDefinitionModel.objects.exists())
        self.assertFalse(MeterModel.objects.exists())
        self.assertFalse(MeterReadingModel.objects.exists())
        self.assertEqual(
            list(NewInvoice.objects.order_by('pk').values_list(
                'pk',
                'contract_id',
                'total_amount',
                'paid_amount',
                'remaining_amount',
                'status',
            )),
            invoice_snapshot,
        )
        self.assertEqual(
            list(NewPaymentHistory.objects.order_by('pk').values_list(
                'pk',
                'invoice_id',
                'amount',
                'method',
                'transaction_code',
            )),
            payment_snapshot,
        )

        for invoice, detail in (
            (unpaid_invoice, unpaid_detail),
            (partial_invoice, partial_detail),
            (paid_invoice, paid_detail),
        ):
            migrated_detail = NewInvoiceDetail.objects.get(pk=detail.pk)
            lines = NewInvoiceLine.objects.filter(legacy_detail_id=detail.pk).order_by('sort_order')
            self.assertEqual(set(lines.values_list('line_code', flat=True)), self.compatibility_codes)
            self.assertEqual(set(lines.values_list('direction', flat=True)), {'charge'})
            self.assertFalse(lines.exclude(service_definition_id=None, meter_reading_id=None).exists())
            line_total = sum(lines.values_list('amount', flat=True), Decimal('0.00'))
            detail_total = (
                migrated_detail.rent_amount
                + migrated_detail.electricity_amount
                + migrated_detail.water_amount
                + migrated_detail.service_amount
            )
            self.assertEqual(line_total, detail_total)
            self.assertEqual(line_total, NewInvoice.objects.get(pk=invoice.pk).total_amount)

        zero_usage_lines = NewInvoiceLine.objects.filter(legacy_detail_id=partial_detail.pk)
        self.assertEqual(zero_usage_lines.get(line_code='legacy-electricity').quantity, Decimal('0.000'))
        self.assertEqual(zero_usage_lines.get(line_code='legacy-water').quantity, Decimal('0.000'))

        reversed_apps = self.migrate(self.migrate_from)
        ReversedInvoice = reversed_apps.get_model('billing', 'Invoice')
        ReversedInvoiceLine = reversed_apps.get_model('billing', 'InvoiceLine')
        ReversedPaymentHistory = reversed_apps.get_model('billing', 'PaymentHistory')
        self.assertFalse(ReversedInvoiceLine.objects.filter(line_code__in=self.compatibility_codes).exists())
        self.assertTrue(ReversedInvoiceLine.objects.filter(line_code='manual-note').exists())
        self.assertEqual(
            list(ReversedInvoice.objects.order_by('pk').values_list(
                'pk',
                'contract_id',
                'total_amount',
                'paid_amount',
                'remaining_amount',
                'status',
            )),
            invoice_snapshot,
        )
        self.assertEqual(
            list(ReversedPaymentHistory.objects.order_by('pk').values_list(
                'pk',
                'invoice_id',
                'amount',
                'method',
                'transaction_code',
            )),
            payment_snapshot,
        )

    def test_backfill_stops_on_reserved_code_collision_without_partial_writes(self):
        old_apps = self.migrate(self.migrate_from)
        contract = self.create_foundation(old_apps)
        invoice, detail = self.create_invoice_detail(
            old_apps,
            contract,
            month=6,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
            paid_amount=Decimal('0.00'),
            status='unpaid',
        )
        InvoiceLineModel = old_apps.get_model('billing', 'InvoiceLine')
        collision = InvoiceLineModel.objects.create(
            invoice=invoice,
            line_code='legacy-rent',
            line_type='rent',
            direction='charge',
            description='Pre-existing reserved line',
            quantity=Decimal('1.000'),
            unit='month',
            unit_price=detail.rent_amount,
            amount=detail.rent_amount,
            legacy_detail=detail,
        )

        with self.assertRaises(RuntimeError):
            self.migrate(self.migrate_to)

        self.assertEqual(InvoiceLineModel.objects.count(), 1)
        collision.delete()

    def test_backfill_stops_on_total_mismatch_without_partial_writes(self):
        old_apps = self.migrate(self.migrate_from)
        contract = self.create_foundation(old_apps)
        invoice, _detail = self.create_invoice_detail(
            old_apps,
            contract,
            month=6,
            electricity_start=100,
            electricity_end=110,
            water_start=20,
            water_end=22,
            paid_amount=Decimal('0.00'),
            status='unpaid',
        )
        InvoiceModel = old_apps.get_model('billing', 'Invoice')
        InvoiceLineModel = old_apps.get_model('billing', 'InvoiceLine')
        InvoiceModel.objects.filter(pk=invoice.pk).update(total_amount=invoice.total_amount + Decimal('1.00'))

        with self.assertRaises(RuntimeError):
            self.migrate(self.migrate_to)

        self.assertFalse(InvoiceLineModel.objects.exists())
        InvoiceModel.objects.filter(pk=invoice.pk).update(total_amount=invoice.total_amount)
