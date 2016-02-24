from django.conf.urls import patterns, url
from website.apps.api.handlers import BundleHandler, ResourceHandler, EventHandler, LogHandler

from piston.resource import Resource
from auth import KeyAuthentication

auth = KeyAuthentication()
bundles = Resource(handler=BundleHandler, authentication=auth)
resources = Resource(handler=ResourceHandler, authentication=auth)
events = Resource(handler=EventHandler, authentication=auth)

from views import api, api_doc, api_new_key
api_log = Resource(handler=LogHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^log$', api_log, name='app_api_log'),
    url(r'^bundles\.?(?P<emitter_format>.+)?$', bundles),
    url(r'^resources\.?(?P<emitter_format>.+)?$', resources),
    url(r'^events\.?(?P<emitter_format>.+)?$', events),
    url(r'^generate$', api_new_key, name='app_api_new_key'),
    url(r'^doc', api_doc, name='app_api_doc'),
    url(r'^$', api, name='app_api'),
)
