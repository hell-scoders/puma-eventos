from django.contrib import admin
from .models import RecurringPattern
from .models import Event

# Register your models here.
admin.site.register([
    RecurringPattern, Event
])
