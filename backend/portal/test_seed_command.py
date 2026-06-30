from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import F
from django.test import TestCase, override_settings

from accounts.models import UserProfile
from listings.models import RoomListing
from properties.models import Property, Room
from tenants.models import Tenant

from .management.commands.seed_rentease_demo_data import DEMO_PROPERTY_CODE


@override_settings(DEBUG=True)
class DemoSeedPropertyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        owner_user = User.objects.create_user(
            username="owner_test",
            password="local-test-password",
            user_type="OWNER",
        )
        cls.owner = UserProfile.objects.create(
            user=owner_user,
            full_name="Seed Owner",
        )
        tenant_user = User.objects.create_user(
            username="tenant_test",
            password="local-test-password",
            user_type="TENANT",
        )
        Tenant.objects.create(
            account=tenant_user,
            full_name="Seed Tenant",
            citizen_id="SEED-TENANT-PRIMARY",
        )

    def run_seed(self):
        call_command(
            "seed_rentease_demo_data",
            owner_username="owner_test",
            tenant_username="tenant_test",
            stdout=StringIO(),
        )

    def test_seed_is_idempotent_and_links_every_demo_room_to_owner_property(self):
        self.run_seed()
        first_counts = (
            Property.objects.count(),
            Room.objects.count(),
            RoomListing.objects.count(),
            Tenant.objects.count(),
        )

        self.run_seed()

        self.assertEqual(
            (
                Property.objects.count(),
                Room.objects.count(),
                RoomListing.objects.count(),
                Tenant.objects.count(),
            ),
            first_counts,
        )
        demo_property = Property.objects.get(
            owner=self.owner,
            property_code=DEMO_PROPERTY_CODE,
        )
        demo_rooms = Room.objects.filter(
            owner=self.owner,
            room_code__startswith="DEMO-",
        )
        self.assertEqual(demo_rooms.count(), 5)
        self.assertFalse(demo_rooms.filter(property__isnull=True).exists())
        self.assertFalse(demo_rooms.exclude(property__owner=F("owner")).exists())
        self.assertFalse(demo_rooms.exclude(property=demo_property).exists())
