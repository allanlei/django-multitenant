from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connections

from optparse import make_option

from south.management.commands import migrate
from south import db

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings as tenant_settings
from tenant.models import Tenant

import sys
import random
import logging
logger = logging.getLogger(__name__)


class Command(migrate.Command):
    option_list = migrate.Command.option_list + (
        make_option('--dispatch_uid', action='store', dest='dispatch_uid',
            default='migrate'),
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
            if database not in tenant_settings.MULTITENANT_PUBLIC_DATABASES:
                db.dbs[database] = self.get_south_wrapper(database, settings.DATABASES[database]['ENGINE'])
                connect_tenant_provider(self, database)
            
            opts = options.copy()
            opts.update({
                'database': database,
            })
            
            print 'Migrating {database}...'.format(database=database)
            response = super(Command, self).handle(*args, **opts)
            connections[database].close()
            disconnect_tenant_provider(self)

    def get_south_wrapper(self, name, engine):
        module_name = "south.db.%s" % db.engine_modules[engine]
        module = __import__(module_name, {}, {}, [''])
        return module.DatabaseOperations(name)
