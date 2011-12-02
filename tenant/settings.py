from django.conf import settings


MULTITENANT_AUTHENTICATION_BACKENDS = tuple(getattr(settings, 'MULTITENANT_AUTHENTICATION_BACKENDS', (
    'tenant.backends.request.QueryParametersBackend',
    'tenant.backends.DefaultBackend',
)))

MULTITENANT_SYNCDB_ONCREATE = bool(getattr(settings, 'MULTITENANT_SYNCDB_ONCREATE', True))
MULTITENANT_MIGRATE_ONCREATE = bool(getattr(settings, 'MULTITENANT_MIGRATE_ONCREATE', True))

MULTITENANT_TENANT_DATABASE = getattr(settings, 'MULTITENANT_TENANT_DATABASE', 'default')
MULTITENANT_PUBLIC_DATABASES = tuple(getattr(settings, 'MULTITENANT_PUBLIC', (
    'default',
    MULTITENANT_TENANT_DATABASE,
)))

MULTITENANT_PUBLIC = MULTITENANT_PUBLIC_DATABASES










#MULTITENANT_PUBLIC_INCLUDE = tuple(getattr(settings, 'MULTITENANT_PUBLIC_INCLUDE', (
#    'tenant',
#)))

#MULTITENANT_PRIVATE_EXCLUDE = tuple(getattr(settings, 'MULTITENANT_PRIVATE_EXCLUDE', (
#    'tenant',
#)))



#MULTITENANT_PUBLIC_APPS = tuple(getattr(settings, 'MULTITENANT_PUBLIC_APPS', (
#    'tenant',
#)))

#MULTITENANT_PRIVATE_APPS = tuple(getattr(settings, 'MULTITENANT_PRIVATE_APPS', set(settings.INSTALLED_APPS) - set(['tenant'])))






#Change to sync all tables for public/private, but deny read/write based on public/private
#Syncdb tough to change
