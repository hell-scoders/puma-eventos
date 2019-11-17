from django.contrib import admin

from .models import Event
from .models import RecurringPattern

# Register your models here.
admin.site.register([
    RecurringPattern, Event
])
