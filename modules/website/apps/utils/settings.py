from django.utils.translation import ugettext_lazy as _

STATUS_INIT = 0
STATUS_RUNNING = 1
STATUS_PROCESSED = 2
STATUS_FAILED = 3

STATUS = (
    (0, _('init')),
    (1, _('processed')),
    (2, _('failed'))
)

EVENT_ERROR = 0

EVENTS = (
    (0, _(u'Errors')),
)