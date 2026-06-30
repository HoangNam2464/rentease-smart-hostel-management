from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import UserProfile
from billing.models import Invoice, PaymentHistory
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import Notification, RepairRequest
from properties.models import Property, Room
from tenants.models import Tenant


class RoleLoginFlowTests(TestCase):
    password = "local-test-password"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.owner = User.objects.create_user(
            username="role_owner_test",
            password=cls.password,
            user_type="OWNER",
        )
        UserProfile.objects.create(
            user=cls.owner,
            full_name="Chủ trọ kiểm thử",
        )

        cls.tenant = User.objects.create_user(
            username="role_tenant_test",
            password=cls.password,
            user_type="TENANT",
        )
        Tenant.objects.create(
            account=cls.tenant,
            full_name="Khách thuê kiểm thử",
            citizen_id="ROLE-LOGIN-TEST",
        )

        cls.admin = User.objects.create_user(
            username="role_admin_test",
            password=cls.password,
            user_type="ADMIN",
            is_staff=True,
        )

    def assert_role_login(self, user, destination, expected_text=None):
        response = self.client.post(
            "/login/",
            {"username": user.username, "password": self.password},
        )
        self.assertRedirects(response, destination, fetch_redirect_response=False)
        destination_response = self.client.get(destination)
        self.assertEqual(destination_response.status_code, 200)
        if expected_text:
            self.assertContains(destination_response, expected_text)
        self.client.logout()

    def test_owner_login_redirects_to_owner_dashboard(self):
        self.assert_role_login(self.owner, "/owner/dashboard/", "Vận hành hôm nay")

    def test_tenant_login_redirects_to_tenant_dashboard(self):
        self.assert_role_login(self.tenant, "/tenant/dashboard/", "Thông tin thuê phòng")

    def test_admin_login_redirects_to_admin(self):
        self.assert_role_login(self.admin, "/admin/")

    def test_invalid_login_uses_vietnamese_message(self):
        response = self.client.post(
            "/login/",
            {"username": self.owner.username, "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tên đăng nhập hoặc mật khẩu chưa đúng")


class PortalDataIsolationTests(TestCase):
    password = "local-test-password"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner_users = []
        cls.tenant_users = []
        cls.tenants = []
        cls.rooms = []
        cls.contracts = []
        cls.invoices = []
        cls.repairs = []
        cls.listings = []
        cls.viewings = []
        cls.notifications = []

        for suffix in ("A", "B"):
            owner_user = User.objects.create_user(
                username=f"isolation_owner_{suffix.lower()}",
                password=cls.password,
                user_type="OWNER",
            )
            owner_profile = UserProfile.objects.create(
                user=owner_user,
                full_name=f"Owner Isolation {suffix}",
            )
            tenant_user = User.objects.create_user(
                username=f"isolation_tenant_{suffix.lower()}",
                password=cls.password,
                user_type="TENANT",
            )
            tenant = Tenant.objects.create(
                account=tenant_user,
                full_name=f"Tenant Isolation {suffix}",
                citizen_id=f"ISOLATION-{suffix}",
                phone_number=f"090000000{1 if suffix == 'A' else 2}",
            )
            property_record = Property.objects.create(
                owner=owner_profile,
                property_code=f"ISO-PROPERTY-{suffix}",
                name=f"Isolation Property {suffix}",
            )
            room = Room.objects.create(
                owner=owner_profile,
                property=property_record,
                room_code=f"ISO-ROOM-{suffix}",
                room_name=f"Isolation Room {suffix}",
                default_rent=Decimal("5000000.00"),
                status="occupied",
            )
            contract = Contract.objects.create(
                room=room,
                tenant=tenant,
                contract_code=f"ISO-CONTRACT-{suffix}",
                signed_date=date(2026, 1, 1),
                start_date=date(2026, 1, 1),
                end_date=date(2026, 12, 31),
                rent_amount=Decimal("5000000.00"),
                deposit_amount=Decimal("5000000.00"),
                status="active",
            )
            invoice = Invoice.objects.create(
                contract=contract,
                month=6,
                year=2026,
                issued_date=date(2026, 6, 1),
                due_date=date(2026, 6, 10),
                total_amount=Decimal("5000000.00"),
                remaining_amount=Decimal("5000000.00"),
                status=Invoice.STATUS_UNPAID,
            )
            PaymentHistory.objects.create(
                invoice=invoice,
                amount=Decimal("1000000.00"),
                method=PaymentHistory.METHOD_BANK_TRANSFER,
                transaction_code=f"ISO-PAYMENT-{suffix}",
            )
            repair = RepairRequest.objects.create(
                room=room,
                tenant=tenant,
                title=f"ISO-REPAIR-{suffix}",
                description="Isolation test repair",
            )
            listing = RoomListing.objects.create(
                room=room,
                title=f"ISO-LISTING-{suffix}",
                description="Isolation test listing",
                listing_price=Decimal("5000000.00"),
                status=RoomListing.STATUS_PUBLISHED,
                available_from=timezone.localdate(),
            )
            viewing = ViewingRegistration.objects.create(
                listing=listing,
                full_name=f"ISO-VIEWING-{suffix}",
                phone=f"091000000{1 if suffix == 'A' else 2}",
                preferred_date=timezone.localdate() + timedelta(days=1),
            )
            notification = Notification.objects.create(
                tenant=tenant,
                invoice=invoice,
                title=f"ISO-NOTIFICATION-{suffix}",
                message="Isolation test notification",
                notification_type=Notification.TYPE_INVOICE,
            )

            cls.owner_users.append(owner_user)
            cls.tenant_users.append(tenant_user)
            cls.tenants.append(tenant)
            cls.rooms.append(room)
            cls.contracts.append(contract)
            cls.invoices.append(invoice)
            cls.repairs.append(repair)
            cls.listings.append(listing)
            cls.viewings.append(viewing)
            cls.notifications.append(notification)

    def test_owner_lists_exclude_other_owners_data(self):
        self.client.force_login(self.owner_users[0])
        cases = (
            ("/owner/rooms/", "ISO-ROOM-A", "ISO-ROOM-B"),
            ("/owner/contracts/", "ISO-CONTRACT-A", "ISO-CONTRACT-B"),
            ("/owner/invoices/", "INV-202606-ISO-ROOM-A", "INV-202606-ISO-ROOM-B"),
            ("/owner/repairs/", "ISO-REPAIR-A", "ISO-REPAIR-B"),
            ("/owner/listings/", "ISO-LISTING-A", "ISO-LISTING-B"),
            ("/owner/viewing-registrations/", "ISO-VIEWING-A", "ISO-VIEWING-B"),
        )

        for url, own_marker, foreign_marker in cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, own_marker)
                self.assertNotContains(response, foreign_marker)

    def test_owner_detail_routes_return_404_for_other_owners_data(self):
        self.client.force_login(self.owner_users[0])
        foreign_urls = (
            f"/owner/rooms/{self.rooms[1].pk}/",
            f"/owner/tenants/{self.tenants[1].pk}/",
            f"/owner/contracts/{self.contracts[1].pk}/",
            f"/owner/invoices/{self.invoices[1].pk}/",
            f"/owner/repairs/{self.repairs[1].pk}/",
            f"/owner/listings/{self.listings[1].pk}/",
            f"/owner/viewing-registrations/{self.viewings[1].pk}/",
        )

        for url in foreign_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_tenant_lists_exclude_other_tenants_data(self):
        self.client.force_login(self.tenant_users[0])
        cases = (
            ("/tenant/contracts/", "ISO-CONTRACT-A", "ISO-CONTRACT-B"),
            ("/tenant/invoices/", "INV-202606-ISO-ROOM-A", "INV-202606-ISO-ROOM-B"),
            ("/tenant/payments/", "ISO-PAYMENT-A", "ISO-PAYMENT-B"),
            ("/tenant/repairs/", "ISO-REPAIR-A", "ISO-REPAIR-B"),
            ("/tenant/notifications/", "ISO-NOTIFICATION-A", "ISO-NOTIFICATION-B"),
        )

        for url, own_marker, foreign_marker in cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, own_marker)
                self.assertNotContains(response, foreign_marker)

    def test_tenant_detail_routes_return_404_for_other_tenants_data(self):
        self.client.force_login(self.tenant_users[0])
        foreign_urls = (
            f"/tenant/contracts/{self.contracts[1].pk}/",
            f"/tenant/invoices/{self.invoices[1].pk}/",
            f"/tenant/repairs/{self.repairs[1].pk}/",
            f"/tenant/notifications/{self.notifications[1].pk}/",
        )

        for url in foreign_urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_owner_and_tenant_cannot_enter_each_others_portal(self):
        self.client.force_login(self.tenant_users[0])
        self.assertRedirects(
            self.client.get("/owner/rooms/"),
            "/access-denied/",
            fetch_redirect_response=False,
        )

        self.client.force_login(self.owner_users[0])
        self.assertRedirects(
            self.client.get("/tenant/contracts/"),
            "/access-denied/",
            fetch_redirect_response=False,
        )


class OwnerPropertyPortalTests(TestCase):
    password = "local-test-password"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner_users = []
        cls.owner_profiles = []
        cls.properties = []

        for suffix in ("A", "B"):
            user = User.objects.create_user(
                username=f"property_portal_owner_{suffix.lower()}",
                password=cls.password,
                user_type="OWNER",
            )
            profile = UserProfile.objects.create(
                user=user,
                full_name=f"Property Portal Owner {suffix}",
            )
            property_record = Property.objects.create(
                owner=profile,
                property_code=f"PORTAL-PROPERTY-{suffix}",
                name=f"Cơ sở Portal {suffix}",
                address=f"Địa chỉ Portal {suffix}",
                ward=f"Phường {suffix}",
                province_city="TP. Hồ Chí Minh",
            )
            cls.owner_users.append(user)
            cls.owner_profiles.append(profile)
            cls.properties.append(property_record)

        cls.room = Room.objects.create(
            owner=cls.owner_profiles[0],
            property=cls.properties[0],
            room_code="PORTAL-ROOM-A",
            room_name="Phòng Portal A",
            default_rent=Decimal("3000000.00"),
        )

    def property_payload(self, **overrides):
        payload = {
            "property_code": "NEW-PROPERTY",
            "name": "Cơ sở mới",
            "address": "456 Đường Mới",
            "ward": "Phường Mới",
            "province_city": "TP. Hồ Chí Minh",
            "latitude": "",
            "longitude": "",
            "contact_phone": "0901234567",
            "status": Property.STATUS_ACTIVE,
            "house_rules": "Giữ yên tĩnh sau 22 giờ.",
        }
        payload.update(overrides)
        return payload

    def room_payload(self, property_record, **overrides):
        payload = {
            "property": property_record.pk,
            "room_code": "NEW-ROOM",
            "room_name": "Phòng mới",
            "floor": "1",
            "area": "25.00",
            "max_occupants": "2",
            "default_rent": "3500000.00",
            "status": "available",
            "description": "Phòng kiểm thử Property.",
        }
        payload.update(overrides)
        return payload

    def test_property_list_and_detail_are_owner_scoped(self):
        self.client.force_login(self.owner_users[0])

        response = self.client.get("/owner/properties/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cơ sở Portal A")
        self.assertContains(response, "Hoạt động")
        self.assertNotContains(response, "Cơ sở Portal B")
        detail_response = self.client.get(f"/owner/properties/{self.properties[0].pk}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Địa chỉ Portal A")
        self.assertContains(detail_response, "PORTAL-ROOM-A")
        self.assertEqual(
            self.client.get(f"/owner/properties/{self.properties[1].pk}/").status_code,
            404,
        )
        self.assertEqual(
            self.client.get(f"/owner/properties/{self.properties[1].pk}/edit/").status_code,
            404,
        )

    def test_owner_can_create_property_without_choosing_owner(self):
        self.client.force_login(self.owner_users[0])

        response = self.client.post(
            "/owner/properties/new/",
            self.property_payload(),
        )

        self.assertRedirects(response, "/owner/properties/", fetch_redirect_response=False)
        created = Property.objects.get(property_code="NEW-PROPERTY")
        self.assertEqual(created.owner, self.owner_profiles[0])

    def test_property_update_preserves_owner_and_stable_code(self):
        self.client.force_login(self.owner_users[0])

        response = self.client.post(
            f"/owner/properties/{self.properties[0].pk}/edit/",
            self.property_payload(
                property_code="ATTEMPTED-CHANGE",
                name="Cơ sở Portal A đã cập nhật",
            ),
        )

        self.assertRedirects(
            response,
            f"/owner/properties/{self.properties[0].pk}/",
            fetch_redirect_response=False,
        )
        self.properties[0].refresh_from_db()
        self.assertEqual(self.properties[0].owner, self.owner_profiles[0])
        self.assertEqual(self.properties[0].property_code, "PORTAL-PROPERTY-A")
        self.assertEqual(self.properties[0].name, "Cơ sở Portal A đã cập nhật")

    def test_room_form_lists_only_owner_properties(self):
        self.client.force_login(self.owner_users[0])

        response = self.client.get("/owner/rooms/new/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PORTAL-PROPERTY-A")
        self.assertNotContains(response, "PORTAL-PROPERTY-B")

    def test_inconsistent_room_relationship_does_not_expose_foreign_property(self):
        mismatched_room = Room.objects.create(
            owner=self.owner_profiles[0],
            property=self.properties[1],
            room_code="MISMATCHED-ROOM",
            room_name="Phòng dữ liệu sai",
            default_rent=Decimal("3000000.00"),
        )
        self.client.force_login(self.owner_users[0])

        list_response = self.client.get("/owner/rooms/")
        detail_response = self.client.get(f"/owner/rooms/{mismatched_room.pk}/")

        self.assertNotContains(list_response, "Cơ sở Portal B")
        self.assertNotContains(detail_response, "Cơ sở Portal B")
        self.assertContains(detail_response, "Chưa liên kết")

    def test_owner_can_create_room_with_owned_property(self):
        self.client.force_login(self.owner_users[0])

        response = self.client.post(
            "/owner/rooms/new/",
            self.room_payload(self.properties[0]),
        )

        self.assertRedirects(response, "/owner/rooms/", fetch_redirect_response=False)
        room = Room.objects.get(owner=self.owner_profiles[0], room_code="NEW-ROOM")
        self.assertEqual(room.property, self.properties[0])

    def test_room_create_and_update_reject_foreign_property(self):
        self.client.force_login(self.owner_users[0])

        create_response = self.client.post(
            "/owner/rooms/new/",
            self.room_payload(self.properties[1]),
        )
        self.assertEqual(create_response.status_code, 200)
        self.assertContains(create_response, "Cơ sở đã chọn không thuộc quyền quản lý của bạn")
        self.assertFalse(Room.objects.filter(owner=self.owner_profiles[0], room_code="NEW-ROOM").exists())

        update_response = self.client.post(
            f"/owner/rooms/{self.room.pk}/edit/",
            self.room_payload(
                self.properties[1],
                room_code=self.room.room_code,
                room_name="Tên không được lưu",
            ),
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertContains(update_response, "Cơ sở đã chọn không thuộc quyền quản lý của bạn")
        self.room.refresh_from_db()
        self.assertEqual(self.room.property, self.properties[0])
        self.assertEqual(self.room.room_name, "Phòng Portal A")

    def test_room_code_is_scoped_to_selected_property(self):
        second_property = Property.objects.create(
            owner=self.owner_profiles[0],
            property_code="PORTAL-PROPERTY-A2",
            name="Cơ sở Portal A2",
        )
        self.client.force_login(self.owner_users[0])

        allowed_response = self.client.post(
            "/owner/rooms/new/",
            self.room_payload(
                second_property,
                room_code=self.room.room_code,
                room_name="Same code in another Property",
            ),
        )
        self.assertRedirects(allowed_response, "/owner/rooms/", fetch_redirect_response=False)
        self.assertTrue(Room.objects.filter(
            property=second_property,
            room_code=self.room.room_code,
        ).exists())

        duplicate_response = self.client.post(
            "/owner/rooms/new/",
            self.room_payload(
                self.properties[0],
                room_code=self.room.room_code,
                room_name="Duplicate in same Property",
            ),
        )
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertContains(duplicate_response, "Cơ sở này đã có một phòng sử dụng mã này.")
        self.assertEqual(Room.objects.filter(
            property=self.properties[0],
            room_code=self.room.room_code,
        ).count(), 1)

    def test_owner_listing_property_context_and_filter_are_owner_scoped(self):
        second_property = Property.objects.create(
            owner=self.owner_profiles[0],
            property_code="PORTAL-PROPERTY-A2",
            name="Cơ sở Portal A2",
        )
        second_room = Room.objects.create(
            owner=self.owner_profiles[0],
            property=second_property,
            room_code="PORTAL-ROOM-A2",
            room_name="Phòng Portal A2",
            default_rent=Decimal("3200000.00"),
        )
        RoomListing.objects.create(
            room=self.room,
            title="LISTING-PROPERTY-A1",
            description="Tin thuộc cơ sở thứ nhất.",
            listing_price=Decimal("3000000.00"),
            available_from=timezone.localdate(),
        )
        RoomListing.objects.create(
            room=second_room,
            title="LISTING-PROPERTY-A2",
            description="Tin thuộc cơ sở thứ hai.",
            listing_price=Decimal("3200000.00"),
            available_from=timezone.localdate(),
        )
        self.client.force_login(self.owner_users[0])

        response = self.client.get(
            "/owner/listings/",
            {"property": self.properties[0].pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LISTING-PROPERTY-A1")
        self.assertNotContains(response, "LISTING-PROPERTY-A2")
        self.assertNotContains(response, "PORTAL-PROPERTY-B")
