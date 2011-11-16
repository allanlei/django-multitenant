from django.conf import settings



MULTITENANT_ROUTING_HANDLER = getattr(settings, 'MULTITENANT_ROUTING_HANDLER', 'tenant.utils.request_params')
#Used by TenantMiddleware to determine the tenant based off a request object. ie ?tenant=abc or abc.example.com or abc.tenants.example.com
MULTITENANT_TENANT_RETRIEVER = getattr(settings, 'MULTITENANT_TENANT_RETRIEVER', 'tenant.utils.get_tenant')

MULTITENANT_DEFAULT_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'donations',                      # Or path to database file if using sqlite3.
    'USER': 'donations',                      # Not used with sqlite3.
    'PASSWORD': 'donations',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '6432',                      # Set to empty string for default. Not used with sqlite3.
},
