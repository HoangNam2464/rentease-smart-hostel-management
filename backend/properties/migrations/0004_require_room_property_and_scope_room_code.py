import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Count, F


def validate_required_property_data(apps, schema_editor):
    Room = apps.get_model('properties', 'Room')
    rooms = Room.objects.using(schema_editor.connection.alias)

    unlinked_room_id = rooms.filter(property_id__isnull=True).values_list('pk', flat=True).first()
    if unlinked_room_id is not None:
        raise RuntimeError(
            f'Room {unlinked_room_id} has no Property; the required-Property migration cannot continue.'
        )

    duplicate = (
        rooms.values('property_id', 'room_code')
        .annotate(row_count=Count('pk'))
        .filter(row_count__gt=1)
        .order_by('property_id', 'room_code')
        .first()
    )
    if duplicate is not None:
        raise RuntimeError(
            'Duplicate room code '
            f"{duplicate['room_code']} exists in Property {duplicate['property_id']}; "
            'the Property-scoped uniqueness migration cannot continue.'
        )

    mismatched_room_id = (
        rooms.exclude(owner_id=F('property__owner_id'))
        .values_list('pk', flat=True)
        .first()
    )
    if mismatched_room_id is not None:
        raise RuntimeError(
            f'Room {mismatched_room_id} has a Property owned by another owner; '
            'the required-Property migration cannot continue.'
        )


def validate_reverse_owner_uniqueness(apps, schema_editor):
    Room = apps.get_model('properties', 'Room')
    duplicate = (
        Room.objects.using(schema_editor.connection.alias)
        .values('owner_id', 'room_code')
        .annotate(row_count=Count('pk'))
        .filter(row_count__gt=1)
        .order_by('owner_id', 'room_code')
        .first()
    )
    if duplicate is not None:
        raise RuntimeError(
            'Cannot reverse Property-scoped room-code uniqueness while owner '
            f"{duplicate['owner_id']} has duplicate room code {duplicate['room_code']}."
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_backfill_default_properties'),
    ]

    operations = [
        migrations.RunPython(validate_required_property_data, noop),
        migrations.AlterField(
            model_name='room',
            name='property',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='rooms',
                to='properties.property',
            ),
        ),
        migrations.RemoveConstraint(
            model_name='room',
            name='unique_room_code_per_owner',
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(
                fields=('property', 'room_code'),
                name='unique_room_code_per_property',
            ),
        ),
        migrations.RunPython(noop, validate_reverse_owner_uniqueness),
    ]
