import pytz

from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.http import int_to_base36

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from website.apps.tasks import AuthPasswordReset
from website.apps.utils.forms import FieldModalset, FormActions, form_layout, save_changes_button
from website.apps.auth.models import UserProfile

from models import Package

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    package = forms.ModelChoiceField(
        required=True,
        label=_(u'Package'),
        empty_label=u'',
        queryset=Package.objects.all(), 
        to_field_name='title', 
        help_text = _('Please see <a href="/pricing" rel="external">pricing page</a>  for more information.')
    )
    username = forms.RegexField(
        label=_('Username'), 
        max_length=30,
        min_length=3,
        regex=r'^[\w]+$',
        help_text = _("Required. 30 characters or fewer. Letters and digits."),
        error_messages = {'invalid': _("This value may contain only letters and numbers characters.")}
    )
    password1 = forms.CharField(
        label=_('Password'), 
        widget=forms.PasswordInput,
        min_length=3
    )
    timezone = forms.ChoiceField(
        required=True,
        choices=[('','')] + [(x, x) for x in pytz.common_timezones],
        help_text = _('So we can tell you what time errors happen at.'),
        widget=widgets.Select({'class': 'chosen'})
    )
    terms = forms.BooleanField(
       label=_('Accept terms of use'), required=True, initial=False,
       help_text = _('By signing up, you agree to the <a href="/terms" rel="external">terms of use</a>.')
   )

    class Meta:
        model = User
        fields = (
            'package', 'username',
            'password1', 'password2', 'email',
            'timezone', 'terms'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Sign up'),
                'package', 'username', 'password1',
                'password2', 'email', 'timezone', 'terms'
            ),
            form_layout
        )

        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True

        if commit:
            user.save()

        user_profile = user.get_profile()
        user_profile.package = self.cleaned_data["package"]
        user_profile.timezone = self.cleaned_data["timezone"]
        user_profile.save()

        return user

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Reset password'),
                'email'
            ),
            form_layout
        )

        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    def save(self, 
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html',
        use_https=False, token_generator=default_token_generator,
        from_email=None, request=None
    ):
        for user in self.users_cache:
            if user.is_active:
                current_site = Site.objects.get_current()
                site_name = current_site.name
                domain = current_site.domain

                messages.info(request, _(u'Please check your email, for further instructions.'))
                AuthPasswordReset.delay(
                    email_template_name, {
                        'domain': domain,
                        'site_name': site_name,
                        'uid': int_to_base36(user.id),
                        'user': user,
                        'token': token_generator.make_token(user),
                        'protocol': use_https and 'https' or 'http',
                    },
                    _("Password reset on %s" % site_name),
                    user.email
                )

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"), 
        widget=forms.PasswordInput,
        min_length=3
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Enter new password'),
                'new_password1', 'new_password2'
            ),
            form_layout
        )

        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

class UserPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_('New password'), 
        widget=forms.PasswordInput,
        min_length=3
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput
    )

    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'user-password'
        self.helper.form_method = 'post'
        self.helper.form_class = 'well box-shadow'
        self.helper.form_action = reverse('app_auth_profile_password_save')
        self.helper.layout = Layout(
            FieldModalset('old_password', 'new_password1', 'new_password2'),
            Layout(FormActions(save_changes_button))
        )

        super(UserPasswordChangeForm, self).__init__(user, *args, **kwargs)

class UserProfileForm(forms.ModelForm):
    package = forms.ModelChoiceField(
        required=True,
        label=_(u'Package'),
        empty_label=u'',
        queryset=Package.objects.all(), 
        to_field_name='title', 
        help_text = _('Please see <a href="/pricing" rel="external">pricing page</a>  for more information.')
    )

    timezone = forms.ChoiceField(
        required=True,
        choices=[('','')] + [(x, x) for x in pytz.common_timezones],
        help_text = _('So we can tell you what time errors happen at.'),
        widget=widgets.Select({'class': 'chosen'})
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'user-data'
        self.helper.form_method = 'post'
        self.helper.form_class = 'well box-shadow'
        self.helper.form_action = reverse('app_auth_profile_data_save')
        self.helper.layout = Layout(
            FieldModalset('package', 'timezone'),
            Layout(FormActions(save_changes_button))
        )

        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('package', 'timezone')

    def save(self, user=None, commit=True):
        if self.instance:
            self.instance.user = user
        return super(UserProfileForm, self).save(commit)
