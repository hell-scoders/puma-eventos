# Generated by Django 2.2.5 on 2019-11-27 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titulo del evento')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('address', models.CharField(default='Ciudad Universitaria', max_length=100, verbose_name='Dirección del evento')),
                ('start_date', models.DateField(verbose_name='Fecha en que comienza el evento')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Fecha en que termina el evento')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Hora en que comienza el evento')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='Hora en que termina el evento')),
                ('capacity', models.IntegerField(verbose_name='Capacidad del evento')),
                ('is_recurring', models.BooleanField(default=False, verbose_name='El evento es recurrente')),
                ('is_full_day', models.BooleanField(default=False, verbose_name='El evento no tiene un horario definido')),
                ('image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Persona o entidad que es host del evento')),
                ('parent_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Evento originario')),
            ],
        ),
        migrations.CreateModel(
            name='StaffEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecurringPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recurring_type', models.CharField(choices=[('D', 'daily'), ('W', 'weekly'), ('M', 'monthly')], max_length=1)),
                ('separation', models.IntegerField()),
                ('max_occurrences', models.IntegerField()),
                ('day_of_week', models.IntegerField()),
                ('week_of_month', models.IntegerField()),
                ('month_of_year', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.AddConstraint(
            model_name='recurringpattern',
            constraint=models.CheckConstraint(check=models.Q(('day_of_week__gte', 1), ('day_of_week__lte', 7)), name='day_in_range'),
        ),
        migrations.AddConstraint(
            model_name='recurringpattern',
            constraint=models.CheckConstraint(check=models.Q(('week_of_month__gte', 1), ('week_of_month__lte', 5)), name='week_in_range'),
        ),
        migrations.AddConstraint(
            model_name='recurringpattern',
            constraint=models.CheckConstraint(check=models.Q(('month_of_year__gte', 1), ('month_of_year__lte', 12)), name='month_in_range'),
        ),
    ]
