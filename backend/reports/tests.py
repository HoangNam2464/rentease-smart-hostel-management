from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import UserProfile
from listings.models import RoomListing
from properties.models import Property, Room


class PropertyReportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff_user = User.objects.create_user(
            username="property_report_staff",
            password="local-test-password",
            user_type="ADMIN",
            is_staff=True,
        )
        cls.owner_user = User.objects.create_user(
            username="property_report_owner",
            password="local-test-password",
            user_type="OWNER",
        )
        owner = UserProfile.objects.create(
            user=cls.owner_user,
            full_name="Report Owner A",
        )
        second_owner_user = User.objects.create_user(
            username="property_report_owner_b",
            password="local-test-password",
            user_type="OWNER",
        )
        second_owner = UserProfile.objects.create(
            user=second_owner_user,
            full_name="Report Owner B",
        )
        cls.property_a = Property.objects.create(
            owner=owner,
            property_code="REPORT-P-A",
            name="REPORT-PROPERTY-A",
            address="STAFF-ONLY-ADDRESS-A",
        )
        property_b = Property.objects.create(
            owner=second_owner,
            property_code="REPORT-P-B",
            name="REPORT-PROPERTY-B",
            address="STAFF-ONLY-ADDRESS-B",
        )
        room_a = Room.objects.create(
            owner=owner,
            property=cls.property_a,
            room_code="REPORT-ROOM-A",
            room_name="Report Room A",
            default_rent=Decimal("3000000.00"),
        )
        room_b = Room.objects.create(
            owner=second_owner,
            property=property_b,
            room_code="REPORT-ROOM-B",
            room_name="Report Room B",
            default_rent=Decimal("3500000.00"),
        )
        RoomListing.objects.create(
            room=room_a,
            title="REPORT-LISTING-A",
            description="Listing A",
            listing_price=Decimal("3000000.00"),
            status=RoomListing.STATUS_PUBLISHED,
            available_from=timezone.localdate(),
        )
        RoomListing.objects.create(
            room=room_b,
            title="REPORT-LISTING-B",
            description="Listing B",
            listing_price=Decimal("3500000.00"),
            status=RoomListing.STATUS_PUBLISHED,
            available_from=timezone.localdate(),
        )

    def test_staff_can_filter_room_and_listing_reports_by_property(self):
        self.client.force_login(self.staff_user)

        room_response = self.client.get(
            "/reports/rooms/",
            {"property": self.property_a.pk},
        )
        self.assertEqual(room_response.status_code, 200)
        self.assertContains(room_response, "REPORT-ROOM-A")
        self.assertContains(room_response, "REPORT-PROPERTY-A")
        self.assertContains(room_response, "STAFF-ONLY-ADDRESS-A")
        self.assertNotContains(room_response, "REPORT-ROOM-B")

        listing_response = self.client.get(
            "/reports/listings/",
            {"property": self.property_a.pk},
        )
        self.assertEqual(listing_response.status_code, 200)
        self.assertContains(listing_response, "REPORT-LISTING-A")
        self.assertContains(listing_response, "REPORT-PROPERTY-A")
        self.assertNotContains(listing_response, "REPORT-LISTING-B")

    def test_reports_reject_anonymous_and_owner_users(self):
        anonymous_response = self.client.get("/reports/rooms/")
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn("/admin/login/", anonymous_response.url)

        self.client.force_login(self.owner_user)
        owner_response = self.client.get("/reports/listings/")
        self.assertEqual(owner_response.status_code, 302)
        self.assertIn("/admin/login/", owner_response.url)
