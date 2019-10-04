from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView


class LoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('index'))


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')
