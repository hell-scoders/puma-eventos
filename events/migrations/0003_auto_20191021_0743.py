# Generated by Django 2.2.5 on 2019-10-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20191021_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='events/media/pictures'),
        ),
    ]