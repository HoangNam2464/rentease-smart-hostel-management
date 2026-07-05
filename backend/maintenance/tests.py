from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import UserProfile
from billing.models import Invoice
from contracts.models import Contract
from properties.models import Property, Room
from tenants.models import Tenant

from .models import Notification, RepairRequest


class MaintenanceRelationshipInvariantTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        owner_user = get_user_model().objects.create_user(
            username="maintenance_invariant_owner",
            password="local-test-password",
            user_type="OWNER",
        )
        owner = UserProfile.objects.create(user=owner_user, full_name="Maintenance Owner")
        property_record = Property.objects.create(
            owner=owner,
            property_code="MAINTENANCE-PROPERTY",
            name="Maintenance Property",
        )
        cls.rooms = [
            Room.objects.create(
                owner=owner,
                property=property_record,
                room_code=f"MAINTENANCE-{suffix}",
                room_name=f"Maintenance Room {suffix}",
                default_rent="5000000.00",
            )
            for suffix in ("A", "B")
        ]
        cls.tenants = [
            Tenant.objects.create(
                full_name=f"Maintenance Tenant {suffix}",
                citizen_id=f"MAINTENANCE-{suffix}",
            )
            for suffix in ("A", "B")
        ]
        cls.contracts = []
        for index, suffix in enumerate(("A", "B")):
            cls.contracts.append(Contract.objects.create(
                room=cls.rooms[index],
                tenant=cls.tenants[index],
                contract_code=f"MAINTENANCE-CONTRACT-{suffix}",
                signed_date=date(2026, 1, 1),
                start_date=date(2026, 1, 1),
                end_date=date(2026, 12, 31),
                rent_amount="5000000.00",
                status="active",
            ))
        cls.invoice = Invoice.objects.create(
            contract=cls.contracts[0],
            month=6,
            year=2026,
            issued_date=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            total_amount="5000000.00",
            remaining_amount="5000000.00",
            status=Invoice.STATUS_UNPAID,
        )

    def test_repair_request_rejects_tenant_from_unrelated_room(self):
        with self.assertRaises(ValidationError):
            RepairRequest.objects.create(
                room=self.rooms[0],
                tenant=self.tenants[1],
                title="Invalid tenant-room relation",
                description="Must not be persisted",
            )

    def test_notification_rejects_invoice_from_another_tenant(self):
        with self.assertRaises(ValidationError):
            Notification.objects.create(
                tenant=self.tenants[1],
                invoice=self.invoice,
                title="Invalid invoice-tenant relation",
                message="Must not be persisted",
                notification_type=Notification.TYPE_INVOICE,
            )

from django.utils import timezone
from datetime import timedelta
from .models import MaintenanceRecord

class MaintenanceRecordLifecycleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        owner_user = get_user_model().objects.create_user(
            username="maintenance_owner",
            password="local-test-password",
            user_type="OWNER",
        )
        owner = UserProfile.objects.create(user=owner_user, full_name="Maintenance Owner")
        property_record = Property.objects.create(
            owner=owner,
            property_code="MAINTENANCE-PROP",
            name="Maintenance Prop",
        )
        cls.room1 = Room.objects.create(
            owner=owner,
            property=property_record,
            room_code="RM-1",
            room_name="Room 1",
            default_rent="5000000.00",
        )
        cls.room2 = Room.objects.create(
            owner=owner,
            property=property_record,
            room_code="RM-2",
            room_name="Room 2",
            default_rent="5000000.00",
        )
        cls.repair_request1 = RepairRequest.objects.create(
            room=cls.room1,
            title="Fix AC",
            description="AC is not cooling.",
            priority=RepairRequest.PRIORITY_MEDIUM,
            status=RepairRequest.STATUS_PENDING,
        )

    def test_repair_request_room_mismatch(self):
        record = MaintenanceRecord(
            room=self.room2,
            repair_request=self.repair_request1,
            maintenance_type="AC Repair",
            description="Test description",
            status=MaintenanceRecord.STATUS_SCHEDULED,
        )
        with self.assertRaises(ValidationError) as ctx:
            record.clean()
        self.assertIn('repair_request', ctx.exception.error_dict)

    def test_completed_requires_completed_at(self):
        record = MaintenanceRecord(
            room=self.room1,
            maintenance_type="AC Repair",
            description="Test description",
            status=MaintenanceRecord.STATUS_COMPLETED,
            completed_at=None,
        )
        with self.assertRaises(ValidationError) as ctx:
            record.clean()
        self.assertIn('completed_at', ctx.exception.error_dict)

    def test_completed_at_cannot_be_before_started_at(self):
        now = timezone.now()
        record = MaintenanceRecord(
            room=self.room1,
            maintenance_type="AC Repair",
            description="Test description",
            status=MaintenanceRecord.STATUS_COMPLETED,
            started_at=now,
            completed_at=now - timedelta(hours=1),
        )
        with self.assertRaises(ValidationError) as ctx:
            record.clean()
        self.assertIn('completed_at', ctx.exception.error_dict)

    def test_valid_completed_record(self):
        now = timezone.now()
        record = MaintenanceRecord(
            room=self.room1,
            maintenance_type="AC Repair",
            description="Test description",
            status=MaintenanceRecord.STATUS_COMPLETED,
            started_at=now - timedelta(hours=1),
            completed_at=now,
        )
        # Should not raise
        record.clean()
