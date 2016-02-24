from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from website.apps.utils.forms import FieldModalset
from models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('email', 'subject', 'message')
        
    def __init__(self, user, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'feedback'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('site_feedback_save')
        self.helper.layout = Layout(
            FieldModalset('email', 'subject', 'message')
        )

        super(FeedbackForm, self).__init__(*args, **kwargs)

        if user.is_authenticated():
            self.fields['email'].widget = forms.HiddenInput()

    def save(self, user, commit=True):
        if user.is_authenticated():
            self.instance.user = user
            self.instance.email = user.email

        return super(FeedbackForm, self).save(commit)
