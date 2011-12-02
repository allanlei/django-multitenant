from django.conf import settings as django_settings
from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from south.management.commands import migrate
from south import db

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings

class Command(migrate.Command):
    option_list = migrate.Command.option_list + (
        make_option('--dispatch_uid', action='store', dest='dispatch_uid',
            default='migrate'),
    )
    
    def handle(self, *args, **options):
        database = options.get('database', 'default')
        dispatch_uid = options.pop('dispatch_uid', 'migrate')
        
        if database not in settings.MULTITENANT_PUBLIC_DATABASES:
            self.south_hack(database)
            connect_tenant_provider(dispatch_uid, database)

        response = super(Command, self).handle(*args, **options)
        disconnect_tenant_provider(dispatch_uid)
        return response

    def south_hack(self, database):
        module_name = "south.db.%s" % db.engine_modules.get(django_settings.DATABASES[database]['ENGINE'], None)
        module = __import__(module_name, {}, {}, [''])
        db.dbs[database] = module.DatabaseOperations(database)
