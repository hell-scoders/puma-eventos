# Generated by Django 2.2.5 on 2019-12-02 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userdetail_event_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff_event',
            field=models.BooleanField(default=False, verbose_name='staff_event status'),
        ),
    ]