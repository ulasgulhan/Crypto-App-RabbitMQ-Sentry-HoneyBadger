# Generated by Django 4.2.11 on 2024-03-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_okxapi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiendpoints',
            name='method',
            field=models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=200),
        ),
    ]
