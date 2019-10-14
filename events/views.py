from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Event

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader



class EventListView(ListView):
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = 'active'
        return context


class EventDetailView(DetailView):
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = 'active'
        return context


class EventDeleteView(DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = 'active'
        return context


class EventUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = 'active'
        return context

def map(request,pk,*args):
    print(pk)
    event= Event.objects.filter(id=pk).first()
    print(event)
    template= loader.get_template('events/event_map.html')
    context ={
        'event': event,
    }
    return HttpResponse(template.render(context,request))