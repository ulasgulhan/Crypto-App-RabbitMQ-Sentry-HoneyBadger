# Generated by Django 4.2.11 on 2024-03-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_apiendpoints_crypto_market_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptomarketapicredentials',
            name='access_passphrase',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
