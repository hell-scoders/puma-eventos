from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import date

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


    def clean(self):
        cleaned_data = self.cleaned_data
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if end_date and start_date:
            if end_date < start_date:
                msg = 'El evento no puede terminar en una fecha anterior a la fecha de inicio'
                self._errors['end_date'] = self.error_class([msg])
                del cleaned_data['end_date']
        return cleaned_data

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError("El evento no puede empezar antes de hoy")
        return start_date
