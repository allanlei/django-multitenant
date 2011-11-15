from signals import request_for_read, request_for_write, request_for_syncdb



class TenantRouter(object):
    def get_tenant(self, signal, model, **hints):
        tenant = None
        responses = signal.send(sender=model, **hints)
        for resp in responses:
            if resp[1]:
                tenant = str(resp[1])
        return tenant

    def db_for_read(self, model, **hints):
        return self.get_tenant(request_for_read, model, **hints)
    
    def db_for_write(self, model, **hints):
        return self.get_tenant(request_for_write, model, **hints)
