# Generated by Django 4.2.11 on 2024-03-14 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_okxapi_access_passphrase'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OkxAPI',
        ),
    ]
