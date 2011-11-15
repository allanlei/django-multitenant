from django.conf import settings
from django.core.urlresolvers import get_callable
from django.utils.functional import curry

from signals import request_for_read, request_for_write, request_for_syncdb



tenant_function = get_callable(settings.TENANT_ROUTING_FN)

class TenantMiddleware(object):
    def process_request(self, request):
        request_for_read.connect(curry(tenant_function, request=request), weak=False, dispatch_uid=request)
        request_for_write.connect(curry(tenant_function, request=request), weak=False, dispatch_uid=request)

    def process_response(self, request, response):
        request_for_read.disconnect(weak=False, dispatch_uid=request)
        request_for_write.disconnect(weak=False, dispatch_uid=request)
        return response
