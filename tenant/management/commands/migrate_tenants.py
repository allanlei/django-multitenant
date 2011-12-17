from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.db import connections

from optparse import make_option

from tenant.models import Tenant


class Command(BaseCommand):
    def handle(self, *args, **options):
        for tenant in Tenant.objects.all():
            print 'Migrating {tenant}...'.format(tenant=tenant)
            call_command('migrate', database=tenant.ident)
            print
