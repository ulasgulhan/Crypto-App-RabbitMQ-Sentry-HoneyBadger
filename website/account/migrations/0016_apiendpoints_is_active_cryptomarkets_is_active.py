# Generated by Django 4.2.11 on 2024-03-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_cryptomarketapicredentials_access_passphrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiendpoints',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cryptomarkets',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]