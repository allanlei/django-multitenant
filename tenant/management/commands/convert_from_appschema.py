from django.core.management.base import BaseCommand, CommandError
from django.core.management import get_commands, call_command, load_command_class
from django.db import DEFAULT_DB_ALIAS, connections, transaction
from django.conf import settings

from optparse import make_option

from tenant.models import Tenant


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Database where appschema lives'),

        make_option('--name-column', action='store', dest='name_column',
            default='name', help='Database where appschema lives'),
        make_option('--public-name-column', action='store', dest='public_name_column',
            default='public_name', help='Database where appschema lives'),
    )
    
    def handle(self, *args, **options):
        alias = options.get('database', DEFAULT_DB_ALIAS)
        cursor = connections[alias].cursor()
        cursor.execute('SELECT {name}, {public_name} from appschema_schema'.format(name=options.get('name_column', 'name'), public_name=options.get('public_name_column', 'public_name')))
        
        dbsettings = settings.DATABASES[alias]

        connection_string = 'postgres://{USER}'.format(**dbsettings)
        if 'PASSWORD' in dbsettings: connection_string = connection_string + ':{PASSWORD}'.format(**dbsettings)
        connection_string = connection_string + '@{HOST}'.format(**dbsettings)
        if 'PORT' in dbsettings: connection_string + ':{PORT}'.format(**dbsettings)
        connection_string = connection_string + '/{NAME}'.format(**dbsettings)
        
        for name, public_name in cursor.fetchall():
            print Tenant.objects.get_or_create(name=name, defaults={
                'public_name': public_name,
                'connection': connection_string
            })
