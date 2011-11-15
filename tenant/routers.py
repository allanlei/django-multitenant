from signals import request_for_read, request_for_write, request_for_syncdb
from django.db import connections, transaction




class BaseTenantRouter(object):
    def get_tenant(self, signal, model, **hints):
        tenant = None
        
        responses = signal.send(sender=model, **hints)
        
        for resp in responses:
            if resp[1]:
                tenant = str(resp[1])
        return tenant
        
    def db_for_read(self, model, **hints):
        raise NotImplementedError()
    
    def db_for_write(self, model, **hints):
        raise NotImplementedError()


class MultiDatabaseTenantRouter(BaseTenantRouter):
    def db_for_read(self, model, **hints):
        return self.get_tenant(request_for_read, model, **hints)
    
    def db_for_write(self, model, **hints):
        return self.get_tenant(request_for_write, model, **hints)

class MultiSchemaTenantRouter(BaseTenantRouter):
#    @transaction.commit_on_success
    def db_for_read(self, model, **hints):
        schema = self.get_tenant(request_for_read, model, **hints)
#        print schema
#        cursor = connections['default'].cursor()
#        cursor.execute('SELECT * FROM example_place')
#        transaction.set_dirty()
        return None
        
    @transaction.commit_on_success
    def db_for_write(self, model, **hints):
        schema = self.get_tenant(request_for_write, model, **hints)
        return None
