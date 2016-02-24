from compressor.filters.closure import ClosureCompilerFilter

from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.template import RequestContext

from ajax_validation.views import validate

from website.apps.utils.requests import ajax_required
from forms import FeedbackForm

@require_http_methods(['GET'])
@cache_page
def corejs(request):
    js = render_to_string('javascript/core.js',
        context_instance=RequestContext(request)
    )

    return HttpResponse(
        ClosureCompilerFilter(js).input(),
        mimetype='text/javascript'
    )

@ajax_required
def feedback_validate(request):
    return validate(request, form_class=FeedbackForm, user=request.user)

@require_http_methods(['POST'])
def feedback_save(request):
    form = FeedbackForm(request.user, data=request.POST.copy() or None)

    if form.is_bound and form.is_valid():
        form.save(request.user) 

    return HttpResponse()