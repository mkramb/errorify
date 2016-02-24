from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.contrib import messages

from models import Event
from filters import EventFilter

from website.apps.utils.settings import EVENT_ERROR
from website.apps.bundles.models import Resource

@require_http_methods(['GET'])
@login_required
def events(request):
    if request.user.get_profile().is_expired:
        messages.error(request, _(u'Your account has expired. Please upgrade your package.')) 
        return redirect('app_auth_profile')

    events = Event.api.all(request.user).filter(type=EVENT_ERROR)

    try:
        last_event = Event.api.all(request.user).filter(type=EVENT_ERROR).latest('last_time')
    except Event.DoesNotExist:
        last_event = None

    filters = EventFilter(
        request.GET.copy(), queryset=events,
        defaults={'filter-reviewed':'3'}, prefix='filter'
    )

    return direct_to_template(request, 'events/index.html', {
        'events': filters.qs,
        'filter': filters.form,
        'filter_has_data': filters.has_data,
        'last_uuid': last_event.uuid if last_event else None,
        'page_name': 'events'
    })

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def events_reviewed(request, uuid):
    event = get_object_or_404(Event, uuid=uuid, user=request.user)
    event.reviewed = True
    event.save()

    messages.success(request, _(u'Market selected error reviewed.')) 
    return redirect('app_events_detail', uuid)

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def events_detail(request, uuid):
    event = get_object_or_404(
        Event.objects.select_related(),
        uuid=uuid, user=request.user
    )

    return direct_to_template(request, 'events/detail.html', {
        'event': event,
        'page_name': 'events'
    })

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def events_resources_delete(request, uuid):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    resource.event_set.all().delete()
    messages.success(request, _(u'Cleared all events for selected resource.'))
    redirect_to = request.META.get('HTTP_REFERER', None)

    return HttpResponseRedirect(redirect_to) if redirect_to else redirect('app_events')

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def events_check(request, uuid):
    try:
        last_event = Event.api.all(request.user).filter(type=EVENT_ERROR).latest('last_time')
    except Event.DoesNotExist:
        last_event = None

    return HttpResponse(
        simplejson.dumps(True if last_event and uuid != last_event.uuid else False),
        mimetype='application/json'
    )
