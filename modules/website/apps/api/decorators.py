from django.db.models import F

from piston.decorator import decorator
from piston.utils import rc

def api_throttle():
    @decorator
    def wrap(f, self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.get_profile().used_api >= request.user.get_profile().package.limit_api:
                return rc.THROTTLED

            request.user.get_profile().used_api = F('used_api') + 1
            request.user.get_profile().save()

        return f(self, request, *args, **kwargs)
    return wrap
