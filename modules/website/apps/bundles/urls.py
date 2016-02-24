from django.conf.urls import patterns, url

from views import bundles, bundles_save, bundles_delete, bundles_detail,\
    bundles_resources_save, bundles_resources_delete, bundles_resources_detail, \
    bundles_resources_source_attr, bundles_resources_process, bundles_resources_process_check

from forms import BundleForm

urlpatterns = patterns('',
    url(r'^detail/(?P<uuid>.+)', bundles_detail, name='app_bundles_detail'),
    url(r'^delete/(?P<uuid>.+)', bundles_delete, name='app_bundles_delete'),
    url(r'^resource/process/check/(?P<uuid>.+)',
        bundles_resources_process_check,
        name='app_bundles_resources_process_check'
    ),
    url(r'^resource/download/source/(?P<uuid>.+)\.map.js',
        bundles_resources_source_attr, {'attr_name': 'source_map'},
        name='app_bundles_resources_source_map'
    ),
    url(r'^resource/download/source/(?P<uuid>.+)\.processed.js',
        bundles_resources_source_attr, {'attr_name': 'source_processed'},
        name='app_bundles_resources_source_processed'
    ),
    url(r'^resource/download/source/(?P<uuid>.+)\.js',
        bundles_resources_source_attr, {'attr_name': 'source'},
        name='app_bundles_resources_source'
    ),
    url(r'^resource/process/(?P<uuid>.+)', bundles_resources_process, name='app_bundles_resources_process'),
    url(r'^resource/detail/(?P<uuid>.+)', bundles_resources_detail, name='app_bundles_resources_detail'),
    url(r'^resource/delete/(?P<uuid>.+)', bundles_resources_delete, name='app_bundles_resources_delete'),
    url(r'^resource/save/(?P<uuid>.+)', bundles_resources_save, name='app_bundles_resources_save'),
    url(r'^save/validate',
        'ajax_validation.views.validate', {'form_class': BundleForm},
        'app_bundles_save_validate'
    ),
    url(r'^save', bundles_save, name='app_bundles_save'),
    url(r'^$', bundles, name='app_bundles'),
)
