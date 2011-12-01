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

def connect_tenant_provider(dispatch_uid, tenant):
    signal_function = curry(lambda sender, tenant=None, **kwargs: tenant, tenant=tenant)
    tenant_provider.connect(signal_function, weak=False, dispatch_uid=dispatch_uid, sender=threading.current_thread())

def disconnect_tenant_provider(dispatch_uid):
    tenant_provider.disconnect(weak=False, dispatch_uid=dispatch_uid)

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

def get_public_models():
    from django.db.models import get_model, get_app, get_models, get_apps
    from tenant import settings
    
    models = []
    for item in settings.MULTITENANT_PUBLIC_INCLUDE:
        app, sep, model = item.partition('.')
        if model:
            models.append(get_model(app, model))
        else:
            models.extend(get_models(get_app(app)))
    return models

def get_private_models():
    from django.db.models import get_model, get_app, get_models, get_apps
    from tenant import settings
    
    excluded = []
    for item in settings.MULTITENANT_PRIVATE_EXCLUDE:
        app, sep, model = item.partition('.')
        if model:
            excluded.append(get_model(app, model))
        else:
            excluded.extend(get_models(get_app(app)))
    all_models = []
    for app in get_apps():
        all_models.extend(get_models(app))
    return list(set(all_models) - set(excluded))
