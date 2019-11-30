from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView)
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Event, Tag

from .forms import EventModelForm, TagModelForm
from django.urls import reverse, reverse_lazy 
from django.shortcuts import get_object_or_404

class EventListView(ListView):
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = 'active'
        return context


class MyEventListView(ListView):
    template_name = 'events/my_events.html'
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
        form.instance.host = self.request.user
        print(form.cleaned_data)
        return super().form_valid(form)


class TagCreateView(BSModalCreateView):
    template_name = 'events/tag_create.html'
    form_class = TagModelForm
    success_message='Tag created'
    success_url = reverse_lazy('events:create')

class TagUpdateView(BSModalCreateView):
    template_name = 'events/tag_create.html'
    form_class = TagModelForm
    success_message='Tag created'
    success_url = reverse_lazy('events:list')
