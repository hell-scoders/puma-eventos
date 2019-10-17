from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

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
        widgets={
            'title' : forms.TextInput(
            attrs={'class':'form-control','placeholder':'Título del evento'}
            ),
            'description' : forms.Textarea(
            attrs={'class':'form-control','placeholder':'Descripción del evento'}
            ),
            'latitude' : forms.NumberInput(
            attrs={'class':'form-control','placeholder':'Latitud'}
            ),
            'longitude' : forms.NumberInput(
            attrs={'class':'form-control','placeholder':'Longitud'}
            ),
            'start_date' : DatePickerInput(),
            'end_date' : DatePickerInput(),
            'start_time' : TimePickerInput(),
            'end_time' : TimePickerInput(),
            'capacity' : forms.NumberInput(
            attrs={'class':'form-control','placeholder':'Capacidad'}
            ),
            'host' : forms.Select(
            attrs={'class':'form-control'}
            ),
            'parent_event' : forms.Select(
            attrs={'class':'form-control'}
            ),
            'is_recurring' : forms.CheckboxInput(
            attrs={'class':'form-check-input'}
            ),
            'is_full_day' : forms.CheckboxInput(
            attrs={'class':'form-check-input'}
            ),
        }
