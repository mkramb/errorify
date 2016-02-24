from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('website',),
}

urlpatterns = patterns('',
    url(r'^api/', include('website.apps.api.urls')),
    url(r'^locale.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^backend/su/', include('django_su.urls')),
    url(r'^backend/', include(admin.site.urls)),
    url(r'^bundles/', include('website.apps.bundles.urls')),
    url(r'^events/', include('website.apps.events.urls')),
    url(r'^stats/', include('website.apps.stats.urls')),
    url(r'^auth/', include('website.apps.auth.urls')),
    url(r'^', include('website.apps.site.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'website.urls.error_404'
handler500 = 'website.urls.error_500'

def error_404(request):
    return direct_to_template(request, '404.html')
    
def error_500(request):
    return direct_to_template(request, '500.html')
