# Generated by Django 3.2.7 on 2021-12-14 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20211214_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]