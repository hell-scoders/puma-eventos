from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Event
from .forms import EventModelForm
from django.urls import reverse
from django.shortcuts import get_object_or_404

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
    template_name = 'events/event_delete.html'
    queryset = Event.objects.all()

    def get_success_url(self):
        return reverse('events:list')


class EventUpdateView(UpdateView):
    template_name = 'events/event_edit.html'
    form_class = EventModelForm
    queryset = Event.objects.all()

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)


class EventCreateView(CreateView):
    template_name = 'events/event_create.html'
    form_class = EventModelForm
    queryset = Event.objects.all()

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)
