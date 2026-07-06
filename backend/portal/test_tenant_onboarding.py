from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import UserProfile
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from properties.models import Property, Room
from tenants.models import Tenant


class OwnerTenantOnboardingTests(TestCase):
    password = 'Strong-demo-password-2026!'

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner_user = User.objects.create_user(
            username='onboarding_owner',
            password=cls.password,
            user_type='OWNER',
        )
        cls.owner = UserProfile.objects.create(
            user=cls.owner_user,
            full_name='Chủ trọ onboarding',
        )
        cls.other_owner_user = User.objects.create_user(
            username='other_onboarding_owner',
            password=cls.password,
            user_type='OWNER',
        )
        cls.other_owner = UserProfile.objects.create(
            user=cls.other_owner_user,
            full_name='Chủ trọ khác',
        )

        cls.property = Property.objects.create(
            owner=cls.owner,
            property_code='ONBOARD-PROPERTY',
            name='Nhà trọ onboarding',
        )
        cls.room = Room.objects.create(
            owner=cls.owner,
            property=cls.property,
            room_code='ONBOARD-R01',
            room_name='Phòng onboarding',
            default_rent=Decimal('2500000.00'),
            status='available',
        )
        cls.listing = RoomListing.objects.create(
            room=cls.room,
            title='Phòng onboarding đang trống',
            description='Tin đăng dùng để kiểm thử onboarding.',
            listing_price=Decimal('2500000.00'),
            deposit_amount=Decimal('1000000.00'),
            status=RoomListing.STATUS_PUBLISHED,
            available_from=timezone.localdate(),
        )
        cls.registration = ViewingRegistration.objects.create(
            listing=cls.listing,
            full_name='Người thuê mới',
            phone='0912345678',
            email='new-tenant@example.com',
            preferred_date=timezone.localdate() + timedelta(days=1),
            status=ViewingRegistration.STATUS_CONFIRMED,
        )

    def payload(self, **overrides):
        today = timezone.localdate()
        data = {
            'username': 'new_tenant_account',
            'email': 'new-tenant@example.com',
            'password1': self.password,
            'password2': self.password,
            'full_name': 'Người thuê mới',
            'phone_number': '0912345678',
            'contract_code': 'ONBOARD-CONTRACT-01',
            'signed_date': today.isoformat(),
            'start_date': today.isoformat(),
            'end_date': (today + timedelta(days=365)).isoformat(),
            'rent_amount': '2500000.00',
            'deposit_amount': '1000000.00',
            'payment_cycle': 'monthly',
        }
        data.update(overrides)
        return data

    def onboarding_url(self):
        return reverse(
            'portal:owner_viewing_registration_onboard',
            args=[self.registration.pk],
        )

    def test_owner_can_create_linked_tenant_account_and_active_contract(self):
        self.client.force_login(self.owner_user)

        response = self.client.post(self.onboarding_url(), self.payload())

        user = get_user_model().objects.get(username='new_tenant_account')
        tenant = Tenant.objects.get(account=user)
        contract = Contract.objects.get(contract_code='ONBOARD-CONTRACT-01')
        self.assertRedirects(
            response,
            reverse('portal:owner_contract_detail', args=[contract.pk]),
        )
        self.assertEqual(user.user_type, 'TENANT')
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(tenant.full_name, 'Người thuê mới')
        self.assertTrue(tenant.citizen_id.startswith('PENDING-'))
        self.assertEqual(contract.tenant, tenant)
        self.assertEqual(contract.room, self.room)
        self.assertEqual(contract.status, 'active')

        self.registration.refresh_from_db()
        self.listing.refresh_from_db()
        self.room.refresh_from_db()
        self.assertEqual(self.registration.tenant, tenant)
        self.assertEqual(self.registration.status, ViewingRegistration.STATUS_COMPLETED)
        self.assertEqual(self.listing.status, RoomListing.STATUS_RENTED)
        self.assertEqual(self.room.status, 'occupied')

        self.client.force_login(user)
        tenant_response = self.client.get(reverse('portal:tenant_contracts_list'))
        self.assertEqual(tenant_response.status_code, 200)
        self.assertContains(tenant_response, 'ONBOARD-CONTRACT-01')

    def test_other_owner_cannot_access_onboarding(self):
        self.client.force_login(self.other_owner_user)

        response = self.client.get(self.onboarding_url())

        self.assertEqual(response.status_code, 404)

    def test_pending_registration_cannot_be_onboarded(self):
        self.registration.status = ViewingRegistration.STATUS_PENDING
        self.registration.save(update_fields=['status', 'updated_at'])
        self.client.force_login(self.owner_user)

        response = self.client.post(self.onboarding_url(), self.payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hãy xác nhận hoặc hoàn tất lịch xem')
        self.assertFalse(
            get_user_model().objects.filter(username='new_tenant_account').exists()
        )
        self.assertFalse(Contract.objects.filter(contract_code='ONBOARD-CONTRACT-01').exists())

    def test_failure_rolls_back_account_profile_and_contract(self):
        User = get_user_model()
        blocker_user = User.objects.create_user(
            username='placeholder_blocker',
            password=self.password,
            user_type='TENANT',
        )
        Tenant.objects.create(
            account=blocker_user,
            full_name='Placeholder blocker',
            citizen_id=f'PENDING-{self.registration.pk:012d}',
        )
        self.client.force_login(self.owner_user)

        response = self.client.post(self.onboarding_url(), self.payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dữ liệu chưa được tạo')
        self.assertFalse(User.objects.filter(username='new_tenant_account').exists())
        self.assertFalse(Contract.objects.filter(contract_code='ONBOARD-CONTRACT-01').exists())
        self.registration.refresh_from_db()
        self.assertIsNone(self.registration.tenant)

    def test_successful_registration_cannot_be_onboarded_twice(self):
        self.client.force_login(self.owner_user)
        first_response = self.client.post(self.onboarding_url(), self.payload())
        self.assertEqual(first_response.status_code, 302)
        user_count = get_user_model().objects.count()
        tenant_count = Tenant.objects.count()
        contract_count = Contract.objects.count()

        response = self.client.post(
            self.onboarding_url(),
            self.payload(
                username='second_tenant_account',
                email='second@example.com',
                contract_code='ONBOARD-CONTRACT-02',
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'đã được liên kết với một người thuê')
        self.assertEqual(get_user_model().objects.count(), user_count)
        self.assertEqual(Tenant.objects.count(), tenant_count)
        self.assertEqual(Contract.objects.count(), contract_count)
