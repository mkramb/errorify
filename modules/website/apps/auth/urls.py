from django.conf.urls import patterns, url
from django.contrib.auth.views import logout_then_login, password_reset
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from forms import UserPasswordResetForm, UserCreateForm, UserProfileForm
from views import sign_in, sign_up, reset_confirm, profile, \
    profile_password_save, profile_data_save, profile_password_validate

password_reset_dict = {
    'template_name': 'auth/reset.html',
    'post_reset_redirect': '/auth/sign-in',
    'email_template_name': 'auth/reset_email.html',
    'password_reset_form' : UserPasswordResetForm,
}

urlpatterns = patterns('',
    url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', reset_confirm, name='app_auth_reset_confirm'),
    url(r'^sign-in/validate', 'ajax_validation.views.validate', {'form_class': AuthenticationForm}, 'app_auth_sign_in_validate'),
    url(r'^sign-up/validate', 'ajax_validation.views.validate', {'form_class': UserCreateForm}, 'app_auth_sign_up_validate'),
    url(r'^sing-out', logout_then_login, {'login_url': settings.LOGIN_URL}, name='app_auth_sign_out'),
    url(r'^sign-in', sign_in, name='app_auth_sign_in'),
    url(r'^sign-up', sign_up, name='app_auth_sign_up'),
    url(r'^reset', password_reset, password_reset_dict, name='app_auth_reset'),
    url(r'^profile/password/validate', profile_password_validate, name='app_auth_profile_password_validate'),
    url(r'^profile/data/validate', 'ajax_validation.views.validate', {'form_class': UserProfileForm}, 'app_auth_profile_data_validate'),
    url(r'^profile/password/save', profile_password_save, name='app_auth_profile_password_save'),
    url(r'^profile/data/save', profile_data_save, name='app_auth_profile_data_save'),
    url(r'^profile', profile, name='app_auth_profile'),
)
