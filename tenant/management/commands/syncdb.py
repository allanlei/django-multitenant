from django.db import transaction, connections

from south.management.commands import syncdb
from optparse import make_option

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings
from tenant.models import Tenant

import sys
import random
import logging
logger = logging.getLogger(__name__)


class Command(syncdb.Command):
    option_list = syncdb.Command.option_list + (
        make_option('--dispatch_uid', action='store', dest='dispatch_uid',
            default='syncdb'),
        make_option('--all_tenants', action='store_true', dest='all_tenants',
            default=False),
    )
    
    def handle(self, *args, **options):
        all_tenants = options.pop('all_tenants')
        dispatch_uid = options.pop('dispatch_uid')
        databases = []
        
        database = options.pop('database')
        if database == '-':
            databases.extend(map(lambda i: i.strip(), sys.stdin.readlines()))
        elif all_tenants:
            databases.extend([tenant['name'] for tenant in Tenant.objects.values('name')])
        else:
            databases.append(database)
        
        random.shuffle(databases)
        for database in databases:
            if database not in settings.MULTITENANT_PUBLIC_DATABASES:
                connect_tenant_provider(dispatch_uid, database)
            
            opts = options.copy()
            opts.update({
                'database': database,
            })
            
            print 'Syncdb {database}...'.format(database=database)
            response = super(Command, self).handle(*args, **opts)
            connections[database].close()
            disconnect_tenant_provider(dispatch_uid)
#        return response
