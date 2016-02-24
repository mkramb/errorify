import base64

from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages

from models import Api

@login_required
@require_http_methods(['GET'])
@user_passes_test(lambda u: not u.get_profile().is_expired)
def api(request):
    api = Api.objects.get(user=request.user)

    return direct_to_template(request, 'api/index.html', {
        'key': base64.encodestring(api.key),
        'page_name': 'api'
    })

@login_required
@require_http_methods(['GET'])
@user_passes_test(lambda u: not u.get_profile().is_expired)
def api_doc(request):
    api = Api.objects.get(user=request.user)
    
    return direct_to_template(request, 'api/doc.html', {
        'key': base64.encodestring(api.key),
        'page_name': 'doc'
    })

@login_required
@require_http_methods(['GET'])
@user_passes_test(lambda u: not u.get_profile().is_expired)
def api_new_key(request):
    api = Api.objects.get(user=request.user)

    if api:
        api.key = api._meta.get_field('key').create_uuid()
        api.save()
        messages.success(request, _(u'Generated new API key.')) 

    return redirect('app_api')
