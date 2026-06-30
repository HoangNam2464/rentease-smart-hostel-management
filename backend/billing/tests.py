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
from .services import generate_invoice, record_payment


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

        detail.save()
        detail.refresh_from_db()
        invoice.refresh_from_db()
        self.assertEqual(detail.electricity_unit_price, Decimal("9999.00"))
        self.assertEqual(detail.water_unit_price, Decimal("88888.00"))
        self.assertEqual(detail.service_amount, Decimal("777777.00"))
        self.assertEqual(invoice.total_amount, Decimal("6055543.00"))

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
