from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import UserProfile
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
