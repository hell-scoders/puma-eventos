# Generated by Django 2.2.5 on 2019-10-23 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_is_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]