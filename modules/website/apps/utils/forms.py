from django.utils.translation import ugettext as _

from crispy_forms.layout import Layout, HTML
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Fieldset

submit_button = HTML('<button class="btn" type="submit"><i class="icon-ok"></i> %s</button>' % _('Submit'))
save_changes_button = HTML('<button class="btn" type="submit"><i class="icon-ok"></i> %s</button>' % _('Save changes'))

form_layout = Layout(
    FormActions(
        submit_button
    )
)

class FieldModalset(Fieldset):
    def __init__(self, *fields, **kwargs):
        super(FieldModalset, self).__init__('', *fields, **kwargs)
        self.template = 'form/modal.html'
        self.legend = False
