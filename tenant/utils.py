import urlparse


def subdomain(sender, request=None, **kwargs):
    if request and 'HTTP_HOST' in request.META:
        host = request.META['HTTP_HOST'].split(':')[1]
        subdomain = '.'.join(host.split('.')[:-1])
        return subdomain
        
def request_params(sender, request=None, **kwargs):
    if request:
        return request.GET.get('tenant', None)
