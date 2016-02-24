from django.utils.translation import ugettext_lazy as _

from models import Bundle
import django_filters

class BundleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_type='icontains', min_length=3, label=_(u'Title'))
    domain = django_filters.CharFilter(lookup_type='icontains', min_length=3, label=_(u'Domain'))

    class Meta:
        model = Bundle
        fields = ['title', 'domain']
