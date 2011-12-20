from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections

from optparse import make_option

import sys


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
        
        cursor.execute('SELECT {name} from appschema_schema'.format(name=options.get('name_column', 'name')))
        
        for appschema in cursor.fetchall():
            print appschema[0]
