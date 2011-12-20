from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.management import call_command

from tenant.models import Tenant

from optparse import make_option
import sys


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--syncdb', action='store_true', dest='syncdb', default=False),
        make_option('--migrate', action='store_true', dest='migrate', default=False),
        make_option('--stdin', action='store_true', dest='stdin', default=False),
#        make_option('-T', '--no-transaction', action='store_false', dest='transaction', default=False),
    )
    
    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 0)
        args = list(args)
        
        if options.get('stdin'):
            args.extend(map(lambda i: i.strip(), sys.stdin.readlines()))

        with transaction.commit_on_success():
            for name in args:
                tenant, created = Tenant.objects.get_or_create(name=name)
                if options['syncdb']:
                    call_command('syncdb', database=tenant.ident, interactive=False, verbosity=verbosity)
                        
                    if options['migrate']:
                        call_command('migrate', database=tenant.ident, interactive=False, verbosity=verbosity)
