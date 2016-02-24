from django.conf.urls import patterns, url
from views import stats_event

urlpatterns = patterns('',
    url(r'^event', stats_event, name='app_stats_event'),
)
