from django.conf import settings


MULTITENANT_SYNCDB_ONCREATE = bool(getattr(settings, 'MULTITENANT_SYNCDB_ONCREATE', False))
MULTITENANT_MIGRATE_ONCREATE = bool(getattr(settings, 'MULTITENANT_MIGRATE_ONCREATE', False))

MULTITENANT_TENANT_DATABASE = getattr(settings, 'MULTITENANT_TENANT_DATABASE', 'default')
MULTITENANT_PUBLIC_DATABASES = tuple(getattr(settings, 'MULTITENANT_PUBLIC', (
    MULTITENANT_TENANT_DATABASE,
))) + tuple(settings.DATABASES.keys())
MULTITENANT_PUBLIC_DATABASES = tuple(set(MULTITENANT_PUBLIC_DATABASES))


_max_tenants = getattr(settings, 'MULTITENANT_MAX_TENANTS', 50)

MULTITENANT_LIMIT_TENANT_CONNECTIONS = bool(getattr(settings, 'MULTITENANT_LIMIT_TENANT_CONNECTIONS', True))
MULTITENANT_MAX_TENANTS = isinstance(_max_tenants, int) and {MULTITENANT_TENANT_DATABASE: _max_tenants} or _max_tenants
MULTITENANT_DESTROY_CONNECTION_ON_REMOVE = bool(getattr(settings, 'MULTITENANT_DESTROY_CONNECTION_ON_REMOVE', True))        #Should leave @ True or you will have to restart the process to remove connections??



MULTITENANT_PUBLIC_APPS = tuple(getattr(settings, 'MULTITENANT_PUBLIC_APPS', ('tenant', )))
MULTITENANT_PUBLIC_APPS_EXCLUDE = tuple(getattr(settings, 'MULTITENANT_PUBLIC_APPS_EXCLUDE', ()))
MULTITENANT_PRIVATE_APPS = tuple(settings.MULTITENANT_PRIVATE_APPS) if getattr(settings, 'MULTITENANT_PRIVATE_APPS', None) is not None else None
MULTITENANT_PRIVATE_APPS_EXCLUDE = tuple(getattr(settings, 'MULTITENANT_PRIVATE_APPS_EXCLUDE', ('tenant', )))
