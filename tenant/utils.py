from django.utils.functional import curry

from tenant.signals import tenant_provider

import threading
import urlparse

import logging
logger = logging.getLogger(__name__)


def get_current_tenant(sender=None, **hints):
    if sender is None:
        sender = threading.current_thread()
    
    tenant = None
    
    responses = tenant_provider.send(sender=sender, **hints)
    for resp in responses:
        if resp[1]:
            tenant = str(resp[1])
            break
    return tenant

def get_tenant(sender, tenant=None, **kwargs):
    return tenant
    
def connect_tenant_provider(dispatch_uid, tenant, sender=None):
    if sender is None:
        sender = threading.current_thread()
    signal_function = curry(get_tenant, tenant=tenant)
    tenant_provider.connect(signal_function, weak=False, dispatch_uid=dispatch_uid, sender=sender)
    return dispatch_uid


def disconnect_tenant_provider(dispatch_uid, sender=None):
    if sender is None:
        sender = threading.current_thread()
    tenant_provider.disconnect(weak=False, dispatch_uid=dispatch_uid, sender=sender)




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

def get_public_apps():
    from django.db.models import get_models, get_app, get_apps
    from tenant import settings
#    from django.db.models.loading import cache as appcache
    
    if settings.MULTITENANT_PUBLIC_APPS is not None:
        include = [app.split('.')[-1] for app in settings.MULTITENANT_PUBLIC_APPS]
#        for app in settings.MULTITENANT_PUBLIC_APPS:
#            app = app.split('.')[-1]
#            include.extend(get_models(get_app(app)))
    else:
        include = [app_mod.__name__.split('.')[-2] for app_mod in get_apps()]
    
    if settings.MULTITENANT_PUBLIC_APPS_EXCLUDE is not None:
        exclude = [app.split('.')[-1] for app in settings.MULTITENANT_PUBLIC_APPS_EXCLUDE]
        
#        exclude = []
#        for app in settings.MULTITENANT_PUBLIC_APPS_EXCLUDE:
#            app = app.split('.')[-1]
#            exclude.extend(get_models(get_app(app)))
    else:
        exclude = []
    return list(set(include) - set(exclude))

def get_private_apps():
    from django.db.models import get_models, get_app, get_apps
    from tenant import settings
    
    if settings.MULTITENANT_PRIVATE_APPS is not None:
        include = [app.split('.')[-1] for app in settings.MULTITENANT_PRIVATE_APPS]
        
#        include = []
#        for app in settings.MULTITENANT_PRIVATE_APPS:
#            app = app.split('.')[-1]
#            include.extend(get_models(get_app(app)))
    else:
        include = [app_mod.__name__.split('.')[-2] for app_mod in get_apps()]
    
    if settings.MULTITENANT_PRIVATE_APPS_EXCLUDE is not None:
        exclude = [app.split('.')[-1] for app in settings.MULTITENANT_PRIVATE_APPS_EXCLUDE]
        
#        exclude = []
#        for app in settings.MULTITENANT_PRIVATE_APPS_EXCLUDE:
#            app = app.split('.')[-1]
#            exclude.extend(get_models(get_app(app)))
    else:
        exclude = []
    return list(set(include) - set(exclude))
