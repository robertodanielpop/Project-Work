# Generated by Django 3.2.7 on 2021-12-13 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20211212_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]