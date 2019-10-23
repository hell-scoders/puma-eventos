from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView
from django import views
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode

from accounts.models import UserDetail
from accounts.tokens import account_activation_token
from .forms import CustomUserCreationForm, CustomAuthenticationForm, StaffUserForm, StaffUserCompleteSignUp

User = get_user_model()


class LoginView(BSModalLoginView):
    """Renders log in form"""
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_message = 'You were successfully logged in.'


class SignUpView(BSModalCreateView):
    """Renders sign up form"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_message = "Thank you for signing up! Please check your email. We've sent you a confirmation email " \
                      "that'll help us verify your identity."
    success_url = reverse_lazy('index')


class CreateStaffUserView(UserPassesTestMixin, views.View):
    form_class = StaffUserForm
    template = "accounts/staff_user_create.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.request = request  # inject request into form
        if form.is_valid():
            form.save()
        context = dict()
        context['form'] = form
        return render(request, self.template, context)

    def get(self, request, *args, **kwargs):
        context = dict()
        context['form'] = self.form_class()
        return render(request, self.template, context)

    def test_func(self):
        return self.request.user.is_superuser


def activate_normal_user(request, uidb64, token):
    """Activates the user account that corresponds to the given token"""
    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:email_confirmed')
    else:
        return HttpResponse('Activation link is invalid!')


class ActivateStaffUser(views.View):
    """Activates the user account that corresponds to the given token"""
    template = "accounts/staff_user_create.html"
    token_generator = PasswordResetTokenGenerator()

    @property
    def user(self):
        return self.request.user

    def get(self, request, uidb64, token):
        try:
            uid = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_staff = True
            user.save()
            login(request, user)

            token = self.token_generator.make_token(user)
            form = StaffUserCompleteSignUp()
            form.user = user  # inject user
            context = {
                'form': form,
                'token': token
            }
            return render(request, 'accounts/staff_user_detail_create.html', context)
        else:
            return HttpResponseBadRequest('Activation link is invalid!')

    @login_required
    def post(self, request, token):
        if self.user and self.token_generator.check_token(self.user, token):
            form = StaffUserCompleteSignUp(request.POST, request.FILES)
            form.user = self.user  # inject user
            if form.is_valid():
                form.save()
                login(request, self.user)
                return redirect('accounts:email_confirmed')
            else:
                token = self.token_generator.make_token(self.user)
                context = {
                    'form': form,
                    'token': token
                }
                return render(request, 'accounts/staff_user_detail_create.html', context)
        else:
            return HttpResponseBadRequest('Activation link is invalid!')


@login_required
def email_confirmed(request):
    """Renders a page that notifies the user that they've registered correctly"""
    return render(request, 'accounts/email_confirmed.html')


@login_required
def user_profile(request):
    """Renders the user's profile"""
    context = dict()
    if request.method != 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    user_detail = UserDetail.objects.get(user_id=request.user.pk)
    context['user_detail'] = user_detail
    context['profile'] = 'active'
    context['image_url'] = user_detail.profile_picture.url if user_detail.profile_picture else static(
        '/img/missing_avatar.png')
    return render(request, 'accounts/user_detail.html', context)
