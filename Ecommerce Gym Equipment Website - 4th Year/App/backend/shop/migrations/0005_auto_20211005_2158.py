# Generated by Django 3.2.7 on 2021-10-05 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
