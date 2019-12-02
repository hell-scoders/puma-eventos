from django import forms
from django_google_maps.widgets import GoogleMapsAddressWidget
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import date, datetime
from django.utils.timezone import now, localtime
from bootstrap_modal_forms.forms import BSModalForm

from .models import Event,Tag
from accounts.models import *

class EventModelForm(forms.ModelForm):
    class Meta(object):
        model = Event
        fields=[
            'title',
            'description',
            'address',
            'geolocation',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'capacity',
            'tags',
            'staff',
            'image',
        ]
        widgets={
            'title' : forms.TextInput(
                attrs={'class':'form-control','placeholder':'Title'}
            ),
            'description' : forms.Textarea(
                attrs={'class':'form-control','placeholder':'Description'}
            ),            
            'address' : GoogleMapsAddressWidget(attrs={'size':'20'}),
            'geolocation':forms.TextInput(attrs={'readonly':'true'}),
            'start_date' : DatePickerInput(attrs={'id':'start_date'}),
            'end_date' : DatePickerInput(attrs={'id':'end_date'}),
            'start_time' : TimePickerInput(attrs={'id':'start_time'}),
            'end_time' : TimePickerInput(attrs={'id':'end_time'}),
            'capacity' : forms.NumberInput(
                attrs={'class':'form-control','placeholder':'Capacity'}
            ),
            'tags' : forms.SelectMultiple(
                attrs={'class':'form-control'}
            ),
            'staff' : forms.SelectMultiple(
                attrs={'class':'form-control'}
            ),
            'image' : forms.FileInput(
                attrs={'type':'file','class':'form-control-file'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventModelForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = User.objects.filter(is_staff_event=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if end_date and start_date:
            if end_date < start_date:
                msg = 'start date can\'t greater than end date'
                self._errors['end_date'] = self.error_class([msg])
                del cleaned_data['end_date']

            if end_time and start_time:
                if end_time < start_time and end_date==start_date:
                    msg = 'The event ends the same day, the start time can\'t greater than end time'
                    self._errors['end_time'] = self.error_class([msg])
                    del cleaned_data['end_time']
            

        return cleaned_data

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError("The event can\'t start in past")
        return start_date

    def clean_start_time(self):
        start_date = self.cleaned_data.get('start_date')        
        start_time = self.cleaned_data.get('start_time')
        if start_time < localtime(now()).time() and start_date == date.today():
            raise forms.ValidationError("The event starts today, can\'t start before now")
        return start_time


class TagModelForm(BSModalForm):
    class Meta:
        model = Tag
        fields=['name']
