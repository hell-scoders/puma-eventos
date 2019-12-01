from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token

User = get_user_model()


def send_normal_confirmation_mail(user: User, request: HttpRequest):
    current_site = get_current_site(request)
    mail_subject = 'Activate your puma-eventos account.'
    message = render_to_string('accounts/normal_activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.send()


def send_staff_confirmation_mail(user: User, request: HttpRequest):
    current_site = get_current_site(request)
    mail_subject = 'Activate your puma-eventos staff account.'
    message = render_to_string('accounts/staff_activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.send()
