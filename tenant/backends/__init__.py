from tenant.models import Tenant


class BaseBackend(object):
    supports_anonymous_tenant = False
    
    def authenticate(self):
        raise NotImplementedError

class DefaultBackend(BaseBackend):
    def authenticate(self, name=None):
        try:
            return Tenant.objects.get(name=name)
        except Tenant.DoesNotExist:
            pass
        return None
