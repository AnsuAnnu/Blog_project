# Generated by Django 4.2.20 on 2025-03-19 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='users',
            new_name='user',
        ),
    ]
