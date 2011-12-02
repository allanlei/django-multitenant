from south.management.commands import syncdb
from optparse import make_option

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings


class Command(syncdb.Command):
    option_list = syncdb.Command.option_list + (
        make_option('--dispatch_uid', action='store', dest='dispatch_uid',
            default='syncdb'),
    )
    
    def handle(self, *args, **options):
        database = options.get('database', 'default')        
        dispatch_uid = options.pop('dispatch_uid', 'syncdb')
        
        if database not in settings.MULTITENANT_PUBLIC_DATABASES:
            connect_tenant_provider(dispatch_uid, database)
            
        response = super(Command, self).handle(*args, **options)
        disconnect_tenant_provider(dispatch_uid)
        return response
