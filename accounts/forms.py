import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, password_validation
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from django.contrib import messages

from accounts.mail import send_normal_confirmation_mail, send_staff_confirmation_mail
from accounts.models import UserDetail, AcademicEntity

User: AbstractBaseUser = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form"""

    class Meta:
        model = User
        fields = ['email', 'password']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    """Custom sign up form"""
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    profile_picture = forms.ImageField(required=False)
    academic_entity = forms.ModelChoiceField(AcademicEntity.objects.all())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("unam.mx"):
            raise forms.ValidationError("The provided email does not end with 'unam.mx'")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.request.is_ajax() and commit:
            user = super().save()
            send_normal_confirmation_mail(user, self.request)
            UserDetail.objects.create(
                user_id=user.id,
                academic_entity_id=self.cleaned_data['academic_entity'].id,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                profile_picture=self.cleaned_data['profile_picture']
            )
        return user

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'academic_entity',
                  'profile_picture',
                  'email',
                  'password1',
                  'password2']


class StaffUserForm(forms.Form):
    """Staff user form"""
    email = forms.EmailField()

    def save(self, commit=True):
        form_user = User.objects.filter(email=self.cleaned_data['email']).first()
        user_exists = form_user is not None

        if user_exists:
            if form_user.is_staff:
                if commit:
                    messages.info(self.request, f'User with email "{form_user}" is already a host!')
            else:
                form_user.is_staff = True
                if commit:
                    form_user.save()
                    messages.info(self.request, f'User with email "{form_user}" already exists,'
                                                f' we upgraded their permissions.')
        else:
            form_user = User.objects.create(email=self.cleaned_data['email'])
            form_user.set_password(str(uuid.uuid4()))
            form_user.is_staff = True
            if commit:
                form_user.save()
                send_staff_confirmation_mail(form_user, self.request)
                messages.info(self.request, 'New staff user created, tell them to check their email in order to '
                                            'complete their registration.')
        return form_user


class StaffUserCompleteSignUp(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        user_detail = super().save(commit=False)
        user_detail.user_id = self.user.id
        if commit:
            self.user.save()
            user_detail.save()
        return user_detail

    class Meta:
        model = UserDetail
        fields = [
            'first_name',
            'last_name',
            'academic_entity',
            'profile_picture',
            'password1',
            'password2'
        ]
