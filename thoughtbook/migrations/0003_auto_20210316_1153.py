# Generated by Django 3.1.4 on 2021-03-16 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thoughtbook', '0002_auto_20210316_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thoughts',
            old_name='owner',
            new_name='user',
        ),
    ]
