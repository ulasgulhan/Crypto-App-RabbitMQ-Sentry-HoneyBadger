# Generated by Django 4.2.11 on 2024-03-14 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_apiendpoints_endpoint_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiendpoints',
            name='endpoint_params',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
