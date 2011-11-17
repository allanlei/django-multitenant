from django.utils.functional import curry

from tenant.signals import tenant_provider

import threading
import os
import sys
import urlparse


def get_current_tenant(sender=None, **hints):
    if sender is None:
        sender = threading.current_thread()
        
    tenant = None
    responses = tenant_provider.send(sender=sender, **hints)
    for resp in responses:
        if resp[1]:
            tenant = str(resp[1])
    return tenant

def connect_tenant_provider(request, tenant):
    signal_function = curry(lambda sender, tenant=None, **kwargs: tenant, tenant=tenant)
    tenant_provider.connect(signal_function, weak=False, dispatch_uid=request, sender=threading.current_thread())

def disconnect_tenant_provider(request):
    tenant_provider.disconnect(weak=False, dispatch_uid=request)
    request.tenant = None

def parse_connection_string(string):
    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('mysql')
    urlparse.uses_netloc.append('postgresql_psycopg2')

    url = urlparse.urlparse(string)
    settings = {
        'NAME':     url.path[1:],
        'USER':     url.username,
        'PASSWORD': url.password,
        'HOST':     url.hostname,
        'PORT':     url.port,
    }
    if url.scheme == 'postgres' or url.scheme == 'postgresql_psycopg2':
        settings['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    if url.scheme == 'mysql':
        settings['ENGINE'] = 'django.db.backends.mysql'
    if not getattr(settings, 'ENGINE', None):
        raise Exception('DATABASE.ENGINE missing')
    return settings
