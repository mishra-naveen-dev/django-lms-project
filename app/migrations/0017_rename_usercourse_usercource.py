# Generated by Django 4.2.6 on 2024-03-12 20:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0016_usercourse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserCourse',
            new_name='UserCource',
        ),
    ]