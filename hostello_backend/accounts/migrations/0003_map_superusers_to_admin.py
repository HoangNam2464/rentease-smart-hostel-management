from django.db import migrations


def forwards_map_superusers_to_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(is_superuser=True).update(user_type='ADMIN')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_user_type_userprofile'),
    ]

    operations = [
        migrations.RunPython(forwards_map_superusers_to_admin, migrations.RunPython.noop),
    ]
