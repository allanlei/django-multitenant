from django.conf import settings

from south.management.commands import migrate
from south import db

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider



class Command(migrate.Command):
    def handle(self, *args, **options):
        database = options.get('database', 'default')
        
        if database == 'default':
            return super(Command, self).handle(*args, **options)
            
        self.south_hack(database)
        
        connect_tenant_provider('migrate', database)
        return super(Command, self).handle(*args, **options)

    def south_hack(self, database):
        module_name = "south.db.%s" % db.engine_modules.get(settings.DATABASES[database]['ENGINE'], None)
        module = __import__(module_name, {}, {}, [''])
        db.dbs[database] = module.DatabaseOperations(database)
