from django.core.urlresolvers import get_callable
from django.utils.functional import curry

import settings
from signals import request_for_read, request_for_write, request_for_syncdb


tenant_routing_pattern = get_callable(settings.MULTITENANT_ROUTING_HANDLER)
get_tenant = get_callable(settings.MULTITENANT_TENANT_RETRIEVER)


class TenantMiddleware(object):
    def process_request(self, request):
        print 'Request %s' % request.get_full_path()
        tenant = get_tenant(request)
        if tenant:
            request.tenant = tenant
            #Signal new_tenant
            
            request_for_read.connect(curry(tenant_routing_pattern, request=request), weak=False, dispatch_uid=request)
            request_for_write.connect(curry(tenant_routing_pattern, request=request), weak=False, dispatch_uid=request)

    def process_response(self, request, response):
        request_for_read.disconnect(weak=False, dispatch_uid=request)
        request_for_write.disconnect(weak=False, dispatch_uid=request)
        print '\tResponse %s' % request.get_full_path()
        return response
