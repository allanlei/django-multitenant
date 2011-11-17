from tenant.backends import BaseBackend
from tenant.models import Tenant

import urlparse

class SubdomainBackend(BaseBackend):
    def authenticate(self, request=None):
        tenant = None
        if 'HTTP_HOST' in request.META:
            host = request.META['HTTP_HOST'].split(':')[1]
            subdomain = '.'.join(host.split('.')[:-1])
            try:
                tenant = Tenant.objects.get(name=subdomain)
            except Tenant.DoesNotExist:
                pass
        return tenant

class QueryParametersBackend(BaseBackend):
    def authenticate(self, request=None):
        tenant = request.GET.get('tenant', None)

        if tenant:
            try:
                return Tenant.objects.using('default').get(name=tenant)
            except Tenant.DoesNotExist:
                pass
