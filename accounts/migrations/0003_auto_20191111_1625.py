# Generated by Django 2.2.5 on 2019-11-11 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191111_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_organizer',
        ),
        migrations.AddField(
            model_name='user',
            name='is_host_staff',
            field=models.BooleanField(default=False, verbose_name='host_staff status. Event staff'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status. Event host'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_unam_community',
            field=models.BooleanField(default=False, verbose_name='unam_community status. Regular user'),
        ),
    ]