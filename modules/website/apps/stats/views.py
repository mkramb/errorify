from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import simplejson

from website.apps.utils.requests import ajax_required
from website.apps.utils.settings import EVENT_ERROR
from models import StatsEvent 

@ajax_required
@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def stats_event(request):
    response = []

    cache_key = 'stats:event:%s' % request.user.id
    stats = cache.get(cache_key)

    if not stats:
        stats = StatsEvent.api.all(request.user).filter(type=EVENT_ERROR).order_by('date')
        cache.set(cache_key, stats, 60 * 60 * 4)

    for item in stats:
        response.append([
            item.date.strftime('%d.%m.%Y'),
            item.count
        ])

    return HttpResponse(
        simplejson.dumps(response),
        mimetype='application/json'
    )