from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)
    start_date = models.DateField('fecha en que comienza el evento')
    end_date = models.DateField('fecha en que termina el evento',
                                null=True)
    start_time = models.TimeField('hora en que comienza el evento')
    end_time = models.TimeField('hora en que termina el evento',
                                null=True)
    capacity = models.IntegerField('capacidad del evento')
    host = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Persona o entidad que es host del evento')
    parent_event = models.ForeignKey('self',
                                     on_delete=models.CASCADE,
                                     verbose_name='Evento originario',
                                     blank=True,
                                     null=True)
    is_recurring = models.BooleanField('el evento es recurrente',
                                       default=False)
    is_full_day = models.BooleanField('el evento no tiene un horario definido',
                                      default=False)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"id": self.id})

    def __str__(self):
        return f"{self.id} - {self.title} creado por {self.host}"


# es necesario leer el siguiente artículo para entender esta estructura de datos:
# https://www.vertabelo.com/blog/again-and-again-managing-recurring-events-in-a-data-model/
class RecurringPattern(models.Model):
    RECURRING_TYPE = [
        ('D', 'daily'),
        ('W', 'weekly'),
        ('M', 'monthly')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    recurring_type = models.CharField(max_length=1, choices=RECURRING_TYPE)
    separation = models.IntegerField()
    max_occurrences = models.IntegerField()
    day_of_week = models.IntegerField()  # 1 to 7
    week_of_month = models.IntegerField()  # 1 to 5
    month_of_year = models.IntegerField()  # 1 to 12

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(day_of_week__lte=7, day_of_week__gte=1), name='day_in_range'),
            models.CheckConstraint(check=models.Q(week_of_month__lte=5, week_of_month__gte=1), name='week_in_range'),
            models.CheckConstraint(check=models.Q(month_of_year__lte=12, month_of_year__gte=1), name='month_in_range')
        ]


class StaffEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
