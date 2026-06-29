from django.db import migrations, models


DEFAULT_PROPERTY_CODE_PREFIX = 'AUTO-OWNER-'
DEFAULT_PROPERTY_NAME_PREFIX = 'Cơ sở mặc định'


def default_property_code(owner_id):
    return f'{DEFAULT_PROPERTY_CODE_PREFIX}{owner_id}'


def default_property_name(owner):
    display_name = (owner.full_name or '').strip()
    name = f'{DEFAULT_PROPERTY_NAME_PREFIX} - {display_name}' if display_name else DEFAULT_PROPERTY_NAME_PREFIX
    return name[:150]


def validate_room_owner_matches_property(Room, db_alias):
    mismatched_room = (
        Room.objects.using(db_alias)
        .exclude(property_id=None)
        .exclude(owner_id=models.F('property__owner_id'))
        .values_list('pk', flat=True)
        .first()
    )
    if mismatched_room is not None:
        raise RuntimeError(
            f'Room {mismatched_room} has a Property owned by another owner; '
            'the default Property migration cannot continue.'
        )


def forwards(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    Property = apps.get_model('properties', 'Property')
    Room = apps.get_model('properties', 'Room')
    db_alias = schema_editor.connection.alias

    validate_room_owner_matches_property(Room, db_alias)

    for owner in UserProfile.objects.using(db_alias).order_by('pk').iterator():
        property_code = default_property_code(owner.pk)
        if Property.objects.using(db_alias).filter(
            owner_id=owner.pk,
            property_code=property_code,
        ).exists():
            raise RuntimeError(
                f'Property code {property_code} is reserved for the default Property backfill.'
            )

        default_property = Property.objects.using(db_alias).create(
            owner_id=owner.pk,
            property_code=property_code,
            name=default_property_name(owner),
            address=owner.rental_address or '',
            ward='',
            province_city='',
            contact_phone='',
            status='active',
            timezone='Asia/Ho_Chi_Minh',
            house_rules='',
        )
        Room.objects.using(db_alias).filter(
            owner_id=owner.pk,
            property_id__isnull=True,
        ).update(property_id=default_property.pk)

    if Room.objects.using(db_alias).filter(property_id__isnull=True).exists():
        raise RuntimeError('Every existing Room must be linked to a Property after backfill.')

    validate_room_owner_matches_property(Room, db_alias)


def backwards(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    Property = apps.get_model('properties', 'Property')
    Room = apps.get_model('properties', 'Room')
    db_alias = schema_editor.connection.alias

    for owner in UserProfile.objects.using(db_alias).order_by('pk').iterator():
        property_code = default_property_code(owner.pk)
        default_property = Property.objects.using(db_alias).filter(
            owner_id=owner.pk,
            property_code=property_code,
        ).first()
        if default_property is None:
            continue

        if Room.objects.using(db_alias).filter(
            property_id=default_property.pk,
        ).exclude(owner_id=owner.pk).exists():
            raise RuntimeError(
                f'Default Property {default_property.pk} contains a Room owned by another owner; '
                'the migration cannot be reversed safely.'
            )

        Room.objects.using(db_alias).filter(
            owner_id=owner.pk,
            property_id=default_property.pk,
        ).update(property_id=None)
        default_property.delete(using=db_alias)


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_property_room_property_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
