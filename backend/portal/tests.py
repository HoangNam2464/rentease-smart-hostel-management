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
from properties.models import Room
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
            room = Room.objects.create(
                owner=owner_profile,
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
