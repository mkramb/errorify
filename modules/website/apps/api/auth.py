import base64

from django.http import HttpResponse
from website.apps.api.models import Api

class KeyAuthentication(object):
    def is_authenticated(self, request):
        key = request.REQUEST.get('key', None)

        if not key:
            return False

        try:
            key = base64.decodestring(key)
            api = Api.objects.select_related().get(key=key)

            if api and api.status:
                api.touch(request.META.get('REMOTE_ADDR', None))

                if not api.user.get_profile().is_expired:
                    request.user = api.user
                    return True
        except:
            pass

        return False

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp.status_code = 401
        return resp
