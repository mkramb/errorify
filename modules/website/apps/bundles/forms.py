from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout
from crispy_forms.bootstrap import FormActions

from website.apps.utils.forms import FieldModalset
from models import Bundle

class BundleForm(forms.ModelForm):
    domain = forms.URLField(
        max_length=255, 
        verify_exists=True,
        required=False,
        help_text = _('Leave empty to ignore domain check (useful for local testing).')
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'bundle'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('app_bundles_save')
        self.helper.layout = Layout(
            FieldModalset('title', 'domain')
        )

        super(BundleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bundle
        fields = ('title', 'domain')

    def save(self, user=None, commit=True):
        if self.instance:
            self.instance.user = user
        return super(BundleForm, self).save(commit)

class BundleProcessForm(forms.Form):
    add_try_catch = forms.BooleanField(
        initial=False, required=False,
        label=_('Add try/catch blocks'),
        help_text = _('Dynamically add try/catch block to every function.')
    )

    pretty_print = forms.BooleanField(
        initial=False, required=False,
        label=_("Don't minify javascript"),
        help_text=_('Will not optimise and minify your file.')
    )

    def __init__(self, resource_uuid,  *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'process'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('app_bundles_resources_process', args=[resource_uuid])
        self.helper.layout = Layout(
            FieldModalset('add_try_catch', 'pretty_print'),
            Layout(
                FormActions(
                    HTML('<button class="btn" type="submit"><i class="icon-cog"></i> %s</button>' % _('Start processing'))
                )
            )
        )

        super(BundleProcessForm, self).__init__(*args, **kwargs)
