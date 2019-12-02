from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_google_maps.fields import AddressField, GeoLocationField

User = get_user_model()


class Tag(models.Model):
    """Events Tags"""
    name = models.CharField('Tag name',max_length=255, unique=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events:create")
        

class Event(models.Model):
    title = models.CharField('Title',max_length=50)
    description = models.TextField('Description')
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(max_length=200,blank=True)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date',
                                null=True, blank=True)
    start_time = models.TimeField('Start time',
                                  null=True, blank=True)
    end_time = models.TimeField('End time',
                                null=True, blank=True)
    capacity = models.IntegerField('Capacity')
    invitations= models.ManyToManyField(User,related_name='invitations')
    host = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Persona o entidad que es host del evento')
    tags = models.ManyToManyField(Tag)
    staff= models.ManyToManyField(User, related_name='staff_event')
    parent_event = models.ForeignKey('self',
                                     on_delete=models.CASCADE,
                                     verbose_name='Evento originario',
                                     blank=True,
                                     null=True)
    is_recurring = models.BooleanField('El evento es recurrente',
                                       default=False)
    is_full_day = models.BooleanField('El evento no tiene un horario definido',
                                      default=False)
    image = models.ImageField(null=True , blank=True, upload_to='event_images/')
    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.id})

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
