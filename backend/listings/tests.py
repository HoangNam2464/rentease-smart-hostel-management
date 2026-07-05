from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import UserProfile
from properties.models import Property, Room

from .models import RoomListing, ViewingRegistration


class PublicListingPresentationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        owner_user = get_user_model().objects.create_user(
            username="listing_owner_test",
            password="local-test-password",
            user_type="OWNER",
        )
        owner = UserProfile.objects.create(user=owner_user, full_name="Chủ trọ kiểm thử")
        cls.property = Property.objects.create(
            owner=owner,
            property_code="PUBLIC-P001",
            name="Cơ sở Hoa Sữa",
            address="PRIVATE-EXACT-ADDRESS",
            ward="Phường 7",
            province_city="TP. Hồ Chí Minh",
            latitude=Decimal("10.123456"),
            longitude=Decimal("106.654321"),
            contact_phone="0987654321",
            timezone="PRIVATE/TIMEZONE",
            house_rules="PRIVATE-HOUSE-RULES",
        )

        room_one = Room.objects.create(
            owner=owner,
            property=cls.property,
            room_code="FILTER-R1",
            room_name="Phòng gác lửng",
            floor=2,
            area=Decimal("24.00"),
            max_occupants=2,
            default_rent=Decimal("2500000.00"),
        )
        room_two = Room.objects.create(
            owner=owner,
            property=cls.property,
            room_code="FILTER-R2",
            room_name="Phòng studio",
            floor=1,
            area=Decimal("20.00"),
            max_occupants=1,
            default_rent=Decimal("3500000.00"),
        )
        cls.listing_one = RoomListing.objects.create(
            room=room_one,
            title="Phòng gác lửng thoáng",
            description="Có cửa sổ và khu bếp riêng.",
            listing_price=Decimal("2500000.00"),
            deposit_amount=Decimal("2500000.00"),
            status=RoomListing.STATUS_PUBLISHED,
            available_from=date(2026, 7, 1),
        )
        RoomListing.objects.create(
            room=room_two,
            title="Phòng studio yên tĩnh",
            description="Phù hợp một người ở.",
            listing_price=Decimal("3500000.00"),
            deposit_amount=Decimal("3500000.00"),
            status=RoomListing.STATUS_PUBLISHED,
            available_from=date(2026, 7, 5),
        )

    def test_list_uses_grounded_placeholder_and_formats_public_data(self):
        response = self.client.get("/rooms/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2.500.000 ₫")
        self.assertContains(response, "room_bedroom_04.jpg")
        self.assertNotContains(response, "picsum.photos")
        self.assertNotContains(response, "FILTER-R1")

    def test_list_filters_by_query_and_maximum_price(self):
        response = self.client.get("/rooms/", {"q": "gác lửng", "max_price": "3000000"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["listings"]), [self.listing_one])

    def test_list_ignores_non_finite_maximum_price(self):
        response = self.client.get("/rooms/", {"max_price": "NaN"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["listings"]), 2)

    def test_detail_hides_internal_code_and_links_to_registration(self):
        response = self.client.get(f"/rooms/{self.listing_one.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "FILTER-R1")
        self.assertContains(response, f"/rooms/{self.listing_one.pk}/register/")

    def test_public_pages_show_only_public_safe_property_fields(self):
        for url in ("/rooms/", f"/rooms/{self.listing_one.pk}/"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, "Cơ sở Hoa Sữa")
                self.assertContains(response, "Phường 7")
                self.assertContains(response, "TP. Hồ Chí Minh")
                for private_value in (
                    "PRIVATE-EXACT-ADDRESS",
                    "0987654321",
                    "10.123456",
                    "106.654321",
                    "PRIVATE/TIMEZONE",
                    "PRIVATE-HOUSE-RULES",
                ):
                    self.assertNotContains(response, private_value)

    def test_visitor_can_submit_viewing_registration_for_published_listing(self):
        response = self.client.post(
            f"/rooms/{self.listing_one.pk}/register/",
            {
                "full_name": "Khách xem phòng",
                "phone": "0901234567",
                "email": "visitor@example.com",
                "preferred_date": timezone.localdate() + timedelta(days=1),
                "preferred_time": "09:30",
                "note": "Xin xem phòng buổi sáng.",
            },
        )

        self.assertRedirects(
            response,
            f"/rooms/{self.listing_one.pk}/register/success/",
            fetch_redirect_response=False,
        )
        registration = ViewingRegistration.objects.get(listing=self.listing_one)
        self.assertEqual(registration.phone, "0901234567")
        self.assertEqual(registration.status, ViewingRegistration.STATUS_PENDING)

    def test_hidden_listing_cannot_receive_viewing_registration(self):
        self.listing_one.status = RoomListing.STATUS_HIDDEN
        self.listing_one.save()

        response = self.client.get(f"/rooms/{self.listing_one.pk}/register/")

        self.assertEqual(response.status_code, 404)
