from django.conf import settings
from settings import STATUS_INIT, STATUS_RUNNING, STATUS_PROCESSED, STATUS_FAILED

from website.apps.site.forms import FeedbackForm

def site(request):
    return { 
        'PROJECT_URL' : settings.PROJECT_URL,
        'STATUS_INIT' : STATUS_INIT,
        'STATUS_RUNNING' : STATUS_RUNNING,
        'STATUS_PROCESSED' : STATUS_PROCESSED,
        'STATUS_FAILED' : STATUS_FAILED,
        'FEEDBACK_FORM' : FeedbackForm(request.user)
    }
