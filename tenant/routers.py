from tenant import settings
from tenant.utils import get_public_apps, get_private_apps
from tenant.utils import get_current_tenant



class TenantRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'tenant':
            return settings.MULTITENANT_TENANT_DATABASE
            
        tenant = get_current_tenant(model=model, **hints)
#        allowed = []
#        if model not in allowed:
#            return False
        return tenant
        
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'tenant':
            return settings.MULTITENANT_TENANT_DATABASE

        tenant = get_current_tenant(model=model, **hints)
#        allowed = []
#        if model not in allowed:
#            return False
        return tenant

#    def allow_syncdb(self, db, model):
#        app = model._meta.app_label
#        
#        if db in settings.MULTITENANT_PUBLIC_DATABASES:
#            return app in get_public_apps()
#        else:
#            return app in get_private_apps()
#        return None
