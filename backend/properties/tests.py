from decimal import Decimal

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, models, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase

from accounts.models import UserProfile

from .admin import PropertyAdmin, RoomAdminForm
from .models import Property, Room


class PropertyFoundationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owners = []
        for suffix in ("A", "B"):
            user = User.objects.create_user(
                username=f"property_owner_{suffix.lower()}",
                password="local-test-password",
                user_type="OWNER",
            )
            cls.owners.append(UserProfile.objects.create(
                user=user,
                full_name=f"Property Owner {suffix}",
            ))

    def create_property(self, owner, code="PROPERTY-001"):
        return Property.objects.create(
            owner=owner,
            property_code=code,
            name="Cơ sở cho thuê kiểm thử",
            address="123 Đường Kiểm Thử",
            ward="Phường 1",
            province_city="TP. Hồ Chí Minh",
            latitude=Decimal("10.776900"),
            longitude=Decimal("106.700900"),
            contact_phone="0901234567",
        )

    def test_property_uses_vietnam_timezone_and_active_status_by_default(self):
        property_record = self.create_property(self.owners[0])

        self.assertEqual(property_record.timezone, "Asia/Ho_Chi_Minh")
        self.assertEqual(property_record.status, Property.STATUS_ACTIVE)

    def test_address_fields_may_be_empty_during_backfill_transition(self):
        property_record = Property(
            owner=self.owners[0],
            property_code="TRANSITIONAL-PROPERTY",
            name="Cơ sở chuyển tiếp",
        )

        property_record.full_clean()

    def test_property_code_is_unique_within_owner(self):
        self.create_property(self.owners[0])

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_property(self.owners[0])

    def test_same_property_code_is_allowed_for_different_owners(self):
        first = self.create_property(self.owners[0])
        second = self.create_property(self.owners[1])

        self.assertEqual(first.property_code, second.property_code)
        self.assertNotEqual(first.owner_id, second.owner_id)

    def test_room_property_is_required_after_transition(self):
        property_record = self.create_property(self.owners[0])
        room_with_required_property = Room.objects.create(
            owner=self.owners[0],
            property=property_record,
            room_code="TRANSITION-001",
            room_name="Phòng chuyển tiếp",
            default_rent=Decimal("3000000.00"),
        )
        room_with_property = Room.objects.create(
            owner=self.owners[0],
            property=property_record,
            room_code="TRANSITION-002",
            room_name="Phòng đã gắn cơ sở",
            default_rent=Decimal("3500000.00"),
        )

        self.assertEqual(room_with_required_property.property_id, property_record.pk)
        self.assertEqual(room_with_property.property_id, property_record.pk)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Room.objects.create(
                    owner=self.owners[0],
                    property=None,
                    room_code="REQUIRED-ROOM",
                    room_name="Room without Property",
                    default_rent=Decimal("3000000.00"),
                )

    def test_room_code_is_unique_within_property(self):
        first_property = self.create_property(self.owners[0], code="PROPERTY-A")
        second_property = self.create_property(self.owners[0], code="PROPERTY-B")
        Room.objects.create(
            owner=self.owners[0],
            property=first_property,
            room_code="SHARED-CODE",
            room_name="Room in first Property",
            default_rent=Decimal("3500000.00"),
        )
        same_code_other_property = Room.objects.create(
            owner=self.owners[0],
            property=second_property,
            room_code="SHARED-CODE",
            room_name="Room in second Property",
            default_rent=Decimal("3500000.00"),
        )

        self.assertEqual(same_code_other_property.property_id, second_property.pk)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Room.objects.create(
                    owner=self.owners[0],
                    property=first_property,
                    room_code="SHARED-CODE",
                    room_name="Duplicate room",
                    default_rent=Decimal("3500000.00"),
                )

    def test_room_validation_rejects_property_owned_by_another_owner(self):
        foreign_property = self.create_property(self.owners[1])
        room = Room(
            owner=self.owners[0],
            property=foreign_property,
            room_code="MISMATCHED-ROOM",
            room_name="Mismatched Room",
            default_rent=Decimal("3000000.00"),
        )

        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_property_admin_keeps_owner_and_code_readonly_after_creation(self):
        property_record = self.create_property(self.owners[0])
        property_admin = PropertyAdmin(Property, admin.site)

        readonly_fields = property_admin.get_readonly_fields(None, property_record)

        self.assertIn('owner', readonly_fields)
        self.assertIn('property_code', readonly_fields)

    def test_room_admin_rejects_property_owned_by_another_owner(self):
        foreign_property = self.create_property(self.owners[1])
        form = RoomAdminForm(data={
            'owner': self.owners[0].pk,
            'property': foreign_property.pk,
            'room_code': 'ADMIN-ROOM',
            'room_name': 'Admin Room',
            'floor': '',
            'area': '',
            'max_occupants': '1',
            'default_rent': '3000000.00',
            'status': 'available',
            'description': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Cơ sở cho thuê phải thuộc cùng chủ trọ với phòng.', form.errors['property'])


class PropertyMigrationRehearsalTests(TransactionTestCase):
    migrate_from = ('properties', '0001_initial')
    migrate_to = ('properties', '0002_property_room_property_and_more')

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([target])
        return executor.loader.project_state([target]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_existing_room_survives_forward_and_backward_migration(self):
        old_apps = self.migrate(self.migrate_from)
        User = old_apps.get_model('accounts', 'User')
        UserProfile = old_apps.get_model('accounts', 'UserProfile')
        OldRoom = old_apps.get_model('properties', 'Room')

        user = User.objects.create(username='property_migration_owner', user_type='OWNER')
        owner = UserProfile.objects.create(user=user, full_name='Migration Owner')
        room = OldRoom.objects.create(
            owner=owner,
            room_code='MIGRATION-ROOM',
            room_name='Migration Room',
            default_rent=Decimal('3000000.00'),
        )
        original_room_id = room.pk
        original_owner_id = room.owner_id

        new_apps = self.migrate(self.migrate_to)
        NewRoom = new_apps.get_model('properties', 'Room')
        migrated_room = NewRoom.objects.get(pk=original_room_id)
        self.assertEqual(migrated_room.owner_id, original_owner_id)
        self.assertIsNone(migrated_room.property_id)

        reversed_apps = self.migrate(self.migrate_from)
        ReversedRoom = reversed_apps.get_model('properties', 'Room')
        reversed_room = ReversedRoom.objects.get(pk=original_room_id)
        self.assertEqual(reversed_room.owner_id, original_owner_id)


class PropertyBackfillMigrationTests(TransactionTestCase):
    migrate_from = ('properties', '0002_property_room_property_and_more')
    migrate_to = ('properties', '0003_backfill_default_properties')

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([target])
        return executor.loader.project_state([target]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_backfill_links_rooms_and_reverses_without_inventing_location(self):
        old_apps = self.migrate(self.migrate_from)
        User = old_apps.get_model('accounts', 'User')
        UserProfile = old_apps.get_model('accounts', 'UserProfile')
        OldProperty = old_apps.get_model('properties', 'Property')
        OldRoom = old_apps.get_model('properties', 'Room')

        first_user = User.objects.create(username='backfill_owner_a', user_type='OWNER')
        first_owner = UserProfile.objects.create(
            user=first_user,
            full_name='Backfill Owner A',
            rental_address='123 Đường Hiện Hữu',
        )
        second_user = User.objects.create(username='backfill_owner_b', user_type='OWNER')
        second_owner = UserProfile.objects.create(
            user=second_user,
            full_name='Backfill Owner B',
            rental_address='',
        )
        existing_property = OldProperty.objects.create(
            owner=first_owner,
            property_code='EXISTING-PROPERTY',
            name='Cơ sở đã tồn tại',
        )
        unlinked_room = OldRoom.objects.create(
            owner=first_owner,
            room_code='BACKFILL-ROOM',
            room_name='Phòng cần backfill',
            default_rent=Decimal('3000000.00'),
        )
        linked_room = OldRoom.objects.create(
            owner=first_owner,
            property=existing_property,
            room_code='EXISTING-ROOM',
            room_name='Phòng đã liên kết',
            default_rent=Decimal('3500000.00'),
        )
        original_room_owners = dict(OldRoom.objects.values_list('pk', 'owner_id'))

        new_apps = self.migrate(self.migrate_to)
        NewProperty = new_apps.get_model('properties', 'Property')
        NewRoom = new_apps.get_model('properties', 'Room')

        self.assertEqual(NewProperty.objects.count(), 3)
        self.assertEqual(NewRoom.objects.count(), 2)
        first_default = NewProperty.objects.get(
            owner_id=first_owner.pk,
            property_code=f'AUTO-OWNER-{first_owner.pk}',
        )
        second_default = NewProperty.objects.get(
            owner_id=second_owner.pk,
            property_code=f'AUTO-OWNER-{second_owner.pk}',
        )
        self.assertEqual(first_default.address, '123 Đường Hiện Hữu')
        self.assertEqual(first_default.ward, '')
        self.assertEqual(first_default.province_city, '')
        self.assertEqual(second_default.address, '')
        self.assertEqual(second_default.ward, '')
        self.assertEqual(second_default.province_city, '')
        self.assertEqual(NewRoom.objects.get(pk=unlinked_room.pk).property_id, first_default.pk)
        self.assertEqual(NewRoom.objects.get(pk=linked_room.pk).property_id, existing_property.pk)
        self.assertFalse(NewRoom.objects.filter(property_id__isnull=True).exists())
        self.assertFalse(NewRoom.objects.exclude(property_id=None).exclude(
            owner_id=models.F('property__owner_id'),
        ).exists())

        reversed_apps = self.migrate(self.migrate_from)
        ReversedProperty = reversed_apps.get_model('properties', 'Property')
        ReversedRoom = reversed_apps.get_model('properties', 'Room')
        self.assertEqual(ReversedProperty.objects.count(), 1)
        self.assertEqual(ReversedRoom.objects.count(), 2)
        self.assertIsNone(ReversedRoom.objects.get(pk=unlinked_room.pk).property_id)
        self.assertEqual(
            ReversedRoom.objects.get(pk=linked_room.pk).property_id,
            existing_property.pk,
        )
        self.assertEqual(
            dict(ReversedRoom.objects.values_list('pk', 'owner_id')),
            original_room_owners,
        )


class PropertyRequiredMigrationTests(TransactionTestCase):
    migrate_from = ('properties', '0003_backfill_default_properties')
    migrate_to = ('properties', '0004_require_room_property_and_scope_room_code')

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([target])
        return executor.loader.project_state([target]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def create_owner(self, apps, username):
        User = apps.get_model('accounts', 'User')
        UserProfile = apps.get_model('accounts', 'UserProfile')
        user = User.objects.create(username=username, user_type='OWNER')
        return UserProfile.objects.create(user=user, full_name=username)

    def create_property(self, apps, owner, code):
        PropertyModel = apps.get_model('properties', 'Property')
        return PropertyModel.objects.create(
            owner=owner,
            property_code=code,
            name=code,
        )

    def create_room(self, apps, owner, property_record, code):
        RoomModel = apps.get_model('properties', 'Room')
        return RoomModel.objects.create(
            owner_id=owner.pk,
            property_id=property_record.pk,
            room_code=code,
            room_name=code,
            default_rent=Decimal('3000000.00'),
        )

    def test_forward_and_backward_migration_preserve_valid_rooms(self):
        old_apps = self.migrate(self.migrate_from)
        owner = self.create_owner(old_apps, 'required_migration_owner')
        first_property = self.create_property(old_apps, owner, 'REQUIRED-PROPERTY-A')
        second_property = self.create_property(old_apps, owner, 'REQUIRED-PROPERTY-B')
        original_room = self.create_room(old_apps, owner, first_property, 'SHARED-CODE')

        new_apps = self.migrate(self.migrate_to)
        NewRoom = new_apps.get_model('properties', 'Room')
        self.assertFalse(NewRoom._meta.get_field('property').null)
        self.assertEqual(NewRoom.objects.get(pk=original_room.pk).property_id, first_property.pk)

        same_code_other_property = self.create_room(
            new_apps,
            owner,
            second_property,
            'SHARED-CODE',
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_room(new_apps, owner, first_property, 'SHARED-CODE')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                NewRoom.objects.create(
                    owner_id=owner.pk,
                    property_id=None,
                    room_code='NO-PROPERTY',
                    room_name='No Property',
                    default_rent=Decimal('3000000.00'),
                )

        same_code_other_property.delete()
        reversed_apps = self.migrate(self.migrate_from)
        ReversedRoom = reversed_apps.get_model('properties', 'Room')
        self.assertTrue(ReversedRoom._meta.get_field('property').null)
        self.assertEqual(ReversedRoom.objects.get(pk=original_room.pk).property_id, first_property.pk)

    def test_forward_migration_rejects_unlinked_room(self):
        old_apps = self.migrate(self.migrate_from)
        owner = self.create_owner(old_apps, 'unlinked_migration_owner')
        property_record = self.create_property(old_apps, owner, 'UNLINKED-PROPERTY')
        OldRoom = old_apps.get_model('properties', 'Room')
        room = OldRoom.objects.create(
            owner=owner,
            property=None,
            room_code='UNLINKED-ROOM',
            room_name='Unlinked Room',
            default_rent=Decimal('3000000.00'),
        )

        with self.assertRaisesRegex(RuntimeError, 'has no Property'):
            self.migrate(self.migrate_to)

        OldRoom.objects.filter(pk=room.pk).update(property=property_record)
        self.migrate(self.migrate_to)

    def test_forward_migration_rejects_owner_mismatch(self):
        old_apps = self.migrate(self.migrate_from)
        first_owner = self.create_owner(old_apps, 'mismatch_migration_owner_a')
        second_owner = self.create_owner(old_apps, 'mismatch_migration_owner_b')
        first_property = self.create_property(old_apps, first_owner, 'MISMATCH-PROPERTY-A')
        second_property = self.create_property(old_apps, second_owner, 'MISMATCH-PROPERTY-B')
        room = self.create_room(old_apps, first_owner, second_property, 'MISMATCH-ROOM')
        OldRoom = old_apps.get_model('properties', 'Room')

        with self.assertRaisesRegex(RuntimeError, 'owned by another owner'):
            self.migrate(self.migrate_to)

        OldRoom.objects.filter(pk=room.pk).update(property=first_property)
        self.migrate(self.migrate_to)

    def test_forward_migration_rejects_duplicate_property_room_code(self):
        old_apps = self.migrate(self.migrate_from)
        first_owner = self.create_owner(old_apps, 'duplicate_migration_owner_a')
        second_owner = self.create_owner(old_apps, 'duplicate_migration_owner_b')
        property_record = self.create_property(old_apps, first_owner, 'DUPLICATE-PROPERTY')
        self.create_room(old_apps, first_owner, property_record, 'DUPLICATE-CODE')
        duplicate_room = self.create_room(old_apps, second_owner, property_record, 'DUPLICATE-CODE')
        OldRoom = old_apps.get_model('properties', 'Room')

        with self.assertRaisesRegex(RuntimeError, 'Duplicate room code'):
            self.migrate(self.migrate_to)

        OldRoom.objects.filter(pk=duplicate_room.pk).delete()
        self.migrate(self.migrate_to)

    def test_reverse_migration_rejects_duplicate_owner_room_code(self):
        new_apps = self.migrate(self.migrate_to)
        owner = self.create_owner(new_apps, 'reverse_migration_owner')
        first_property = self.create_property(new_apps, owner, 'REVERSE-PROPERTY-A')
        second_property = self.create_property(new_apps, owner, 'REVERSE-PROPERTY-B')
        self.create_room(new_apps, owner, first_property, 'REVERSE-CODE')
        duplicate_room = self.create_room(new_apps, owner, second_property, 'REVERSE-CODE')
        NewRoom = new_apps.get_model('properties', 'Room')

        with self.assertRaisesRegex(RuntimeError, 'Cannot reverse'):
            self.migrate(self.migrate_from)

        NewRoom.objects.filter(pk=duplicate_room.pk).delete()
        self.migrate(self.migrate_from)
