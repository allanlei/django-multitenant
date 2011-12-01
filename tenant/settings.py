from django.conf import settings


MULTITENANT_AUTHENTICATION_BACKENDS = tuple(getattr(settings, 'MULTITENANT_AUTHENTICATION_BACKENDS', (
#    'tenant.backends.SubdomainBackend',
#    'tenant.backends.RequestParametersBackend',
#    'tenant.backends.DefaultBackend',
#    'tenant.backends.TestBackend',
    'tenant.backends.request.QueryParametersBackend',
    'tenant.backends.DefaultBackend',
)))

MULTITENANT_TENANT_DATABASE = getattr(settings, 'MULTITENANT_TENANT_DATABASE', 'default')

MULTITENANT_PUBLIC = tuple(getattr(settings, 'MULTITENANT_PUBLIC', (
    'default',
    MULTITENANT_TENANT_DATABASE,
)))

MULTITENANT_PUBLIC_INCLUDE = tuple(getattr(settings, 'MULTITENANT_PUBLIC_INCLUDE', (
    'south',
    'openid.Association',
    'openid.Nonce',
    'tenant',
)))

MULTITENANT_PRIVATE_EXCLUDE = tuple(getattr(settings, 'MULTITENANT_PRIVATE_EXCLUDE', (
    'tenant',
    'openid.Association',
    'openid.Nonce',
)))





#MULTITENANT_TENANT_IDENTIFIER_HANDLER = getattr(settings, 'MULTITENANT_TENANT_IDENTIFIER_HANDLER', 'tenant.identifiers.query_tenant_identifier')
#MULTITENANT_TENANT_REQUEST_READ = getattr(settings, 'MULTITENANT_TENANT_REQUEST_READ', 'tenant.signals.default_tenant_signal_response')
#MULTITENANT_TENANT_REQUEST_WRITE = getattr(settings, 'MULTITENANT_TENANT_REQUEST_WRITE', 'tenant.signals.default_tenant_signal_response')
#MULTITENANT_TENANT_REQUEST_READ = getattr(settings, 'MULTITENANT_TENANT_REQUEST_READ', 'ttenant.signals.default_tenant_signal_response')
