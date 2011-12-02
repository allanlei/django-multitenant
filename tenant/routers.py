from tenant import settings
#from tenant.utils import get_public_models, get_private_models
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
