from django.core.management.base import BaseCommand

from optparse import make_option

from tenant.models import Tenant


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):
        for tenant in Tenant.objects.all():
            print tenant.ident
