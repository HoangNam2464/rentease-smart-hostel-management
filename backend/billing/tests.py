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
