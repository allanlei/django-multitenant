from tenant.utils import get_current_tenant

class BaseTenantRouter(object):
    pass


class TenantRouter(BaseTenantRouter):
    def db_for_read(self, model, **hints):
        import threading
        tenant = get_current_tenant(model=model, **hints)
        return tenant
        
    def db_for_write(self, model, **hints):
        tenant = get_current_tenant(model=model, **hints)
        return tenant

    def allow_syncdb(self, db, model):
        from tenant import settings
        from tenant.utils import get_public_models, get_private_models
        
        if db in settings.MULTITENANT_PUBLIC:
            included = get_public_models()
        else:
            included = get_private_models()
            
        if model not in included:
            return False
        return False
