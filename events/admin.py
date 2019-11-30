from django.contrib import admin
from .models import RecurringPattern
from .models import Event
from django.forms.widgets import TextInput
from django_google_maps.widgets import GoogleMapsAddressWidget
from django_google_maps.fields import AddressField, GeoLocationField

from events import models


class EventModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {
            'widget': GoogleMapsAddressWidget
        },
        GeoLocationField: {
            'widget': TextInput(attrs={
                'readonly': 'readonly'
            })
        },
    }
# Register your models here.
#admin.site.register([
 #   RecurringPattern, Event
#])

admin.site.register(models.Event, EventModelAdmin)
