from django.utils.translation import ugettext_lazy as _

from models import Event
import django_filters

class EventFilter(django_filters.FilterSet):
    reviewed = django_filters.BooleanFilter(label=_(u'Is reviewed?'))
    last_time = django_filters.DateRangeFilter(label=_(u'Last time'))
    client_browser = django_filters.CharFilter(lookup_type='icontains', min_length=3, label=_(u'Browser'))
    client_url = django_filters.CharFilter(lookup_type='icontains', min_length=3, label=_(u'Website URL'))
       
    class Meta:
        model = Event
        fields = ['reviewed', 'last_time', 'client_browser', 'client_url']
