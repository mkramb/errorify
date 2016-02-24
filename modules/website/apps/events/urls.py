from django.conf.urls import patterns, url
from views import events, events_reviewed, events_detail, events_resources_delete, events_check

urlpatterns = patterns('',
    url(r'^check/(?P<uuid>.+)', events_check, name='app_events_check'),
    url(r'^detail/(?P<uuid>.+)', events_detail, name='app_events_detail'),
    url(r'^reviewed/(?P<uuid>.+)', events_reviewed, name='app_events_reviewed'),
    url(r'^clear/resources/(?P<uuid>.+)', events_resources_delete, name='app_resource_events_delete'),
    url(r'^$', events, name='app_events'),
)
