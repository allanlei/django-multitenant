from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from south.management.commands import migrate
from south import db

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings as tenant_settings

class Command(migrate.Command):
    option_list = migrate.Command.option_list + (
        make_option('--dispatch_uid', action='store', dest='dispatch_uid',
            default='migrate'),
    )
    
    def handle(self, *args, **options):
        database = options['database']
        
        dispatch_uid = options.pop('dispatch_uid')
        
        if database not in tenant_settings.MULTITENANT_PUBLIC_DATABASES:
            db.dbs[database] = self.get_south_wrapper(database, settings.DATABASES[database]['ENGINE'])
            connect_tenant_provider(dispatch_uid, database)

        response = super(Command, self).handle(*args, **options)
        disconnect_tenant_provider(dispatch_uid)
        return response

    def get_south_wrapper(self, name, engine):
        module_name = "south.db.%s" % db.engine_modules[engine]
        module = __import__(module_name, {}, {}, [''])
        return module.DatabaseOperations(name)
