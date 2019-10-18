from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from .views import (
    LoginView,
    SignUpView,
    CreateStaffUserView,
    activate_normal_user,
    ActivateStaffUser,
    email_confirmed,
    user_profile
)

app_name = 'accounts'
urlpatterns = [
    path('profile/', user_profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create_staff_user/', CreateStaffUserView.as_view(), name='create_staff_user'),
    path('email_confirmed/', email_confirmed, name='email_confirmed'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate_normal_user, name='activate_normal_user'),
    re_path(r'^activate_staff/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            ActivateStaffUser.as_view(), name='activate_staff_user'),
    re_path(r'^register_staff_user_detail/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            ActivateStaffUser.as_view(), name='activate_staff_user_post')
]
