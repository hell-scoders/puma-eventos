from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.core.mail import send_mail

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("unam.mx"):
            raise forms.ValidationError("The provided email does not end with 'unam.mx'")
        return email

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
