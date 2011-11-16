import urlparse


    
def subdomain(sender, request=None, **kwargs):
    if request and 'HTTP_HOST' in request.META:
        host = request.META['HTTP_HOST'].split(':')[1]
        subdomain = '.'.join(host.split('.')[:-1])
        return subdomain
        
def request_params(sender, request=None, tenant_key='tenant', **kwargs):
    if request:
        return request.GET.get(tenant_key, None)

def get_tenant(request):
    return request_params(None, request=request)
