from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404

from tenant.models import Tenant
from tenant.utils import connect_tenant_provider, disconnect_tenant_provider


class TenantMiddleware(object):
    def process_request(self, request):
        request.tenant = None
        name = resolve(request.path).kwargs.get('domain') or request.GET.get('tenant')
        
        if name:
            tenant = get_object_or_404(Tenant.objects.using('default'), name=name)
            request.tenant = tenant
            connect_tenant_provider(request, tenant.name)
            
    def process_response(self, request, response):
        disconnect_tenant_provider(request)
        request.tenant = None
        return response
