from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from settings import MULTITENANT_AUTHENTICATION_BACKENDS
from signals import tenant_authenticated


def load_backend(backend):
    try:
        backend_module = '.'.join(backend.split('.')[:-1])
        backend_classname = backend.split('.')[-1]
        backend_class = getattr(import_module(backend_module), backend_classname)
        return backend_class()
    except Exception, e:
        print e
        raise ImproperlyConfigured('Error importing tenant authentication backend %s ' % backend)

def authenticate(**kwargs):
    for backend in MULTITENANT_AUTHENTICATION_BACKENDS:
        backend = load_backend(backend)

        try:
            tenant = backend.authenticate(**kwargs)
        except TypeError:
            continue

        if tenant is None:
            continue
#        from models import Tenant
#        tenant.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        tenant_authenticated.send(sender=backend, tenant=tenant, **kwargs)
        return tenant
    return None
