import pytz

from django.views.generic.simple import direct_to_template
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.utils.http import base36_to_int
from django.shortcuts import redirect
from django.contrib import messages

from ajax_validation.views import validate

from website.apps.utils.requests import ajax_required
from forms import UserCreateForm, UserSetPasswordForm, \
    UserProfileForm, UserPasswordChangeForm

@require_http_methods(['GET','POST'])
@sensitive_post_parameters()
def sign_in(request):
    if request.user.is_authenticated():
        return redirect('app_events')

    redirect_to = request.REQUEST.get('next', None)
    form = AuthenticationForm(data=request.POST.copy() or None)

    if form.is_bound and form.is_valid():
        user = form.get_user()
        if user is not None and user.is_active:
            login(request, user)
            request.session['user_timezone'] = pytz.timezone(request.user.get_profile().timezone)

            if redirect_to:
                return HttpResponseRedirect(redirect_to)
            return redirect('app_events')

    return direct_to_template(request, 'auth/sign_in.html', { 'form': form })

@require_http_methods(['GET', 'POST'])
@sensitive_post_parameters()
def sign_up(request):
    if request.user.is_authenticated():
        return redirect('app_events')

    form = UserCreateForm(data=request.POST.copy() or None)

    if form.is_bound and form.is_valid() and form.save():
        messages.success(request, _(u'Thank you for registering. You are now logged in.')) 
        login(request, authenticate(
            username=request.POST['username'],
            password=request.POST['password1'])
        )
        return redirect('app_events')

    return direct_to_template(request, 'auth/sign_up.html', {'form': form})

@require_http_methods(['GET','POST'])
@sensitive_post_parameters()
def reset_confirm(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    validlink = False
    form = UserSetPasswordForm(None)

    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True

        if request.method == 'POST':
            form = UserSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _(u'You have successfully reseted password, please sign in.')) 
                return redirect('app_auth_sign_in')

    if not validlink:
        raise Http404

    return direct_to_template(request, 'auth/reset_confirm.html', {'form': form})

@require_http_methods(['GET'])
@sensitive_post_parameters()
@login_required
def profile(request):
    return direct_to_template(request, 'auth/profile.html', {
        'form_password': UserPasswordChangeForm(request.user),
        'form_profile': UserProfileForm(initial={
            'package': request.user.get_profile().package if request.user.get_profile().package else 1,
            'timezone': request.user.get_profile().timezone
        })
    })

@require_http_methods(['POST'])
@sensitive_post_parameters()
@login_required
def profile_password_save(request):
    form = UserPasswordChangeForm(request.user, data=request.POST.copy() or None)

    if form.is_bound and form.is_valid() and form.save():
        messages.success(request, _(u'Changed your password.')) 

    return redirect('app_auth_profile')

@ajax_required
@sensitive_post_parameters()
@login_required
def profile_password_validate(request):
    return validate(request, form_class=UserPasswordChangeForm, user=request.user)

@require_http_methods(['POST'])
@login_required
def profile_data_save(request):
    form = UserProfileForm(
        data=request.POST.copy() or None,
        instance=request.user.get_profile()
    )

    if form.is_bound and form.is_valid() and form.save(request.user):
        request.session['user_timezone'] = pytz.timezone(form.data.get('timezone'))
        messages.success(request, _(u'Changed your profile data.')) 

    return redirect('app_auth_profile')

