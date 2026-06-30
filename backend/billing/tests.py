from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import UserProfile
from contracts.models import Contract
from properties.models import Property, Room
from tenants.models import Tenant

from .models import Invoice, InvoiceDetail, PaymentHistory, PriceConfig
from .services import generate_invoice, record_payment


class BillingInvariantTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        owner_user = get_user_model().objects.create_user(
            username="billing_invariant_owner",
            password="local-test-password",
            user_type="OWNER",
        )
        owner = UserProfile.objects.create(user=owner_user, full_name="Billing Owner")
        property_record = Property.objects.create(
            owner=owner,
            property_code="BILLING-PROPERTY",
            name="Billing Property",
        )
        cls.room = Room.objects.create(
            owner=owner,
            property=property_record,
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
