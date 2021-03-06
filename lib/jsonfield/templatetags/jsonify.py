from django import template
from django.utils import simplejson as json
from django.utils.safestring import mark_safe
from jsonfield.utils import TZAwareJSONEncoder

register = template.Library()

@register.filter
def jsonify(value):
    return mark_safe(json.dumps(value, cls=TZAwareJSONEncoder))
