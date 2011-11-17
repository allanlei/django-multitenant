from south.management.commands import migrate

from django.utils.functional import curry

from tenant.signals import request_for_read, request_for_write, request_for_syncdb
from tenant.models import Tenant


class Command(migrate.Command):
    def handle(self, *args, **options):
        database = options.get('database', 'default')
        
        if database == 'default':
            return super(Command, self).handle(*args, **options)
        
        
        tenant = Tenant.objects.using('default').get(name=database)
        
        def tenant_based_route(sender, tenant=None, **kwargs):
            return tenant
            
        request_for_read.connect(curry(tenant_based_route, tenant=tenant), weak=False, dispatch_uid='migrate')
        request_for_write.connect(curry(tenant_based_route, tenant=tenant), weak=False, dispatch_uid='migrate')
        
        return super(Command, self).handle(*args, **options)
        
        request_for_read.disconnect(weak=False, dispatch_uid='migrate')
        request_for_write.disconnect(weak=False, dispatch_uid='migrate')
        
