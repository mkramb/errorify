from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from views import corejs, feedback_validate, feedback_save

urlpatterns = patterns('',
    url(r'^core.js$', corejs),
    url(r'^feedback/validate', feedback_validate, name='site_feedback_validate'),
    url(r'^feedback/save', feedback_save, name='site_feedback_save'),
    url(r'^features$', direct_to_template,
        {'template': 'site/features.html', 'extra_context': {'page_name': 'features'}},
        name='site_features'
    ),
    url(r'^pricing$', direct_to_template,
        {'template': 'site/pricing.html', 'extra_context': {'page_name': 'pricing'}},
        name='site_pricing'
    ),
    url(r'^terms$', direct_to_template,
        {'template': 'site/terms.html', 'extra_context': {'page_name': 'terms'}},
        name='site_terms'
    ),
    url(r'^$', direct_to_template,
        {'template': 'site/home.html'},
        name='site'
    ),
)
