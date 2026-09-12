from django.db import migrations


def create_superadmin(apps, schema_editor):
    UserModel = apps.get_model('user', 'UserModel')

    if not UserModel.objects.filter(email='admin@gmail.com').exists():
        user = UserModel(
            email='admin@gmail.com',
            name='Admin',
            surname='Admin',
            role='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('admin')
        user.save()


def reverse_func(apps, schema_editor):
    UserModel = apps.get_model('user', 'UserModel')
    UserModel.objects.filter(email='admin@gmail.com').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superadmin, reverse_func),
    ]