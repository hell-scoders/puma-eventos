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
from django.shortcuts import get_object_or_404,redirect,render

from pyzbar.pyzbar import decode
from PIL import Image

import qrcode

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

from accounts.models import UserDetail
import os

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
    
def logo_data(img_location):
    logo = MIMEImage(open(img_location,"rb").read(), _subtype="jpg")
    logo.add_header('Content-ID', '<invitation_qr>')
    return logo

def generate_qr_code(event_id,uid):
    qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
    qr.add_data('events/'+str(event_id)+'/invitation/'+str(uid))
    qr.make(fit=True)
    img=qr.make_image()
    img_location="media/event_images/"+str(event_id)+"invitation"+str(uid)+".jpg"
    img.save(img_location)
    return img_location

def send_invitation_mail(event_id,uid,user_detail):
    img_location=generate_qr_code(event_id,uid)
    subject="Invitation to event. Info-puma"
    mail_to = user_detail.user.email
    from_email = os.environ['EMAIL_HOST_USER']
    html_message=render_to_string('events/mail_invitation.html')
    msg=EmailMultiAlternatives(subject,html_message,from_email,[mail_to])
    msg.attach_alternative(html_message,"text/html")
    msg.attach(logo_data(img_location))
    msg.send()

def invitation(request,pk):
    event=Event.objects.get(id=pk)
    context= dict()
    context['result']="Full capped event. Cannot issue invitation :("
    if(event.capacity>event.invitations.count()):
        user_detail = UserDetail.objects.get(user_id=request.user.pk)
        if not request.user in event.invitations.all():
            send_invitation_mail(pk,request.user.pk,user_detail)
            context['result']="Check your mail for your qr code. :)"
            event.invitations.add(user_detail.user)
            user_detail.event_history.add(event)
        else:
            context['result']="Already invited."

    return render(request,'events/invitation_confirmation.html',context)
