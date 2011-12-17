from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

#from south.management.commands import syncdb
from optparse import make_option

from tenant import models

class Command(BaseCommand):    
    def handle(self, *args, **options):
        for tenant in Tenant.objects.all():
            print 'Syncdb on {tenant}'.format(tenant=tenant)
            call_command('syncdb', database=tenant.ident)
            print '\n\n'
