import json
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from billing.models import Invoice, PaymentIntent, PaymentWebhookEvent, PaymentHistory
from accounts.models import UserProfile
from tenants.models import Tenant
from contracts.models import Contract
from properties.models import Property, Room
from django.contrib.auth import get_user_model


class PayOSWebhookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner_user = User.objects.create_user(
            username="payos_owner", password="pwd", user_type="OWNER"
        )
        cls.owner = UserProfile.objects.create(user=cls.owner_user, full_name="Owner")
        
        cls.property = Property.objects.create(
            owner=cls.owner, property_code="P1", name="P1"
        )
        cls.room = Room.objects.create(
            owner=cls.owner, property=cls.property, room_code="R1", default_rent=5000000
        )
        cls.tenant = Tenant.objects.create(full_name="Tenant", citizen_id="123")
        
        cls.contract = Contract.objects.create(
            room=cls.room, tenant=cls.tenant, contract_code="C1",
            signed_date=timezone.now().date(), start_date=timezone.now().date(),
            end_date=timezone.now().date(), rent_amount=5000000, deposit_amount=0,
            status="active"
        )
        
        cls.invoice = Invoice.objects.create(
            contract=cls.contract, month=1, year=2026, total_amount=Decimal('5000000.00'),
            paid_amount=Decimal('0.00'), status=Invoice.STATUS_UNPAID
        )
        
        cls.client = Client()

    def setUp(self):
        self.intent = PaymentIntent.objects.create(
            invoice=self.invoice,
            amount=Decimal('5000000.00'),
            order_code="123456",
            status=PaymentIntent.STATUS_PENDING
        )
        self.url = reverse('billing_api:payos_webhook')

    @patch('billing.gateways.payos_adapter.PayOSGateway.verify_webhook_signature')
    def test_valid_webhook_full_payment(self, mock_verify):
        mock_verify.return_value = True
        
        payload = {
            "code": "00",
            "data": {
                "orderCode": 123456,
                "amount": 5000000,
                "description": "Thanh toan",
                "reference": "REF123"
            }
        }
        
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.intent.refresh_from_db()
        self.assertEqual(self.intent.status, PaymentIntent.STATUS_PAID)
        self.assertEqual(self.intent.payment_history.amount, Decimal('5000000.00'))
        
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.paid_amount, Decimal('5000000.00'))
        self.assertEqual(self.invoice.status, Invoice.STATUS_PAID)

    @patch('billing.gateways.payos_adapter.PayOSGateway.verify_webhook_signature')
    def test_valid_webhook_underpaid_goes_to_review(self, mock_verify):
        mock_verify.return_value = True
        
        payload = {
            "code": "00",
            "data": {
                "orderCode": 123456,
                "amount": 4000000, # Underpaid
                "description": "Thanh toan",
                "reference": "REF123"
            }
        }
        
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.intent.refresh_from_db()
        self.assertEqual(self.intent.status, PaymentIntent.STATUS_REVIEW)
        self.assertIsNone(self.intent.payment_history)
        
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.paid_amount, Decimal('0.00'))
        self.assertEqual(self.invoice.status, Invoice.STATUS_UNPAID)

    @patch('billing.gateways.payos_adapter.PayOSGateway.verify_webhook_signature')
    def test_invalid_signature_rejected(self, mock_verify):
        mock_verify.return_value = False
        
        payload = {
            "code": "00",
            "data": {
                "orderCode": 123456,
                "amount": 5000000
            }
        }
        
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.intent.refresh_from_db()
        self.assertEqual(self.intent.status, PaymentIntent.STATUS_PENDING)

    @patch('billing.gateways.payos_adapter.PayOSGateway.verify_webhook_signature')
    def test_duplicate_webhook_ignored(self, mock_verify):
        mock_verify.return_value = True
        
        payload = {
            "code": "00",
            "data": {
                "orderCode": 123456,
                "amount": 5000000
            }
        }
        
        # First call
        response1 = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        
        # Second call
        response2 = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response2.status_code, 200)
        
        # Ensure only 1 payment history is created
        self.assertEqual(PaymentHistory.objects.filter(invoice=self.invoice).count(), 1)
        
        # But 2 webhook events are recorded
        self.assertEqual(PaymentWebhookEvent.objects.filter(order_code="123456").count(), 2)
