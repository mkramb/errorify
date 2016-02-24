from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib import messages
from django.db import IntegrityError

from models import Bundle, Resource
from filters import BundleFilter
from forms import BundleForm, BundleProcessForm

from website.apps.tasks import ResourceCompile
from website.apps.utils.settings import STATUS_RUNNING, STATUS_PROCESSED
from website.apps.utils.files import is_text_file
from website.apps.utils.requests import ajax_required
from website.apps.api.exceptions import BandwidthOverload
from website.apps.events.filters import EventFilter

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles(request):
    bundles = Bundle.api.all(request.user)
    filters = BundleFilter(request.GET.copy(), queryset=bundles, prefix='filter')

    return direct_to_template(request, 'bundles/index.html', {
        'bundles': filters.qs,
        'filter': filters.form,
        'filter_has_data': filters.has_data,
        'form': BundleForm(),
        'page_name': 'bundles'
    })

@require_http_methods(['POST'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_save(request):
    try:
        form = BundleForm(data=request.POST.copy() or None)

        if form.is_bound and form.is_valid():
            bundle = form.instance
            bundle.user = request.user
            bundle.api_save(request.user)

            messages.success(request, _(u'Added new bundle, please append some resources.'))
            return redirect('app_bundles_detail', bundle.uuid)
    except BandwidthOverload:
        messages.error(request, _(u'You have exceed your quota for domains.'))
        return redirect('app_bundles')
    except IntegrityError:
        messages.error(request, _(u'Bundle for passed domain name already exists.'))
        return redirect('app_bundles')

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_delete(request, uuid):
    get_object_or_404(Bundle, uuid=uuid, user=request.user).api_delete(request.user)
    messages.success(request, _(u'Deleted selected bundle.')) 
    return redirect('app_bundles')

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_detail(request, uuid):
    bundle = get_object_or_404(Bundle, uuid=uuid, user=request.user)
    resources = Resource.api.all(request.user).filter(bundle=bundle).order_by('-created')

    return direct_to_template(request, 'bundles/detail.html', {
        'bundle': bundle,
        'resources': resources,
        'page_name': 'bundles'
    })

@require_http_methods(['POST'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_save(request, uuid):
    response = []

    for uploaded_file in request.FILES.values():
        if is_text_file(uploaded_file):
            resource = Resource(bundle=Bundle.api.get(uuid, request.user))
            resource.source = ''.join([ chunk for chunk in uploaded_file.chunks() ])
            resource.save()
            response.append(resource.uuid)

    if len(response) and not len(messages.get_messages(request)):
        messages.success(request, _(u'New resources uploaded.'))

    if not request.is_ajax():
        return redirect('app_bundles_detail', uuid)

    return HttpResponse(
        simplejson.dumps(response),
        mimetype='application/json'
    )

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_delete(request, uuid):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    resource.delete()
    messages.success(request, _(u'Deleted selected resource.'))

    return redirect('app_bundles_detail', resource.bundle.uuid)

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_detail(request, uuid):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    events = resource.event_set.all()
    filters = EventFilter(
        request.GET.copy(), queryset=events, prefix='filter'
    )

    return direct_to_template(request, 'resources/detail.html', {
        'resource': resource,
        'form': BundleProcessForm(resource.uuid),
        'events': filters.qs,
        'events_filter': filters.form,
        'events_filter_has_data': filters.has_data,
        'page_name': 'bundles'
    })

@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_source_attr(
    request, uuid,
    attr_name='source',
    attr_type='application/javascript; charset=utf8'
):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    return HttpResponse(
        getattr(resource, attr_name),
        content_type = attr_type
    )

@require_http_methods(['POST'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_process(request, uuid):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    form = BundleProcessForm(uuid, data=request.POST.copy() or None)

    if form.is_valid():
        compiler_config = []

        if form.cleaned_data['add_try_catch']:
            compiler_config.append('AddTryCatch')

        if form.cleaned_data['pretty_print']:
            compiler_config.append('PrettyPrint')

        resource.status = STATUS_RUNNING
        resource.save()
        ResourceCompile.delay(resource, compiler_config)

    return redirect('app_bundles_resources_detail', resource.uuid)

@ajax_required
@require_http_methods(['GET'])
@login_required
@user_passes_test(lambda u: not u.get_profile().is_expired)
def bundles_resources_process_check(request, uuid):
    resource = get_object_or_404(
        Resource.objects.select_related(),
        uuid=uuid, bundle__user=request.user
    )

    if resource.is_processed and resource.status == STATUS_PROCESSED:
        messages.success(request, _(u'Resource is successfully processed.'))

    return HttpResponse(
        simplejson.dumps(resource.is_processed),
        mimetype="application/json"
    )
