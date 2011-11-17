from tenant.utils import get_current_tenant


class BaseTenantRouter(object):
    pass


class TenantRouter(BaseTenantRouter):
    def get_private_models(self):
        if not hasattr(self, 'private_models'):
            from django.db.models import get_model, get_app, get_models
            from tenant import settings
            
            self.private_models = []
#            self.private_models = [get_model(model.split('.', 1)) for model in settings.MULTITENANT_PRIVATE_MODELS]
#        print self.private_models
        return self.private_models

    def db_for_read(self, model, **hints):
        import threading
        tenant = get_current_tenant(model=model, **hints)
        return tenant
        
    def db_for_write(self, model, **hints):
        tenant = get_current_tenant(model=model, **hints)
        return tenant

    def allow_syncdb(self, db, model):
        if model in self.get_private_models():
            return False
        return None
