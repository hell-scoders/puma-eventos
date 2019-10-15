from django import forms

from .models import Event


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields=[
                'title',
                'description',
                'latitude',
                'longitude',
                'start_date',
                'end_date',
                'start_time',
                'end_time',
                'capacity',
                'host',
                'parent_event',
                'is_recurring',
                'is_full_day',
        ]
