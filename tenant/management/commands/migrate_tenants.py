from django.core.management import call_command

from tenant.utils import connect_tenant_provider, disconnect_tenant_provider


class Command(migrate.Command):
    def handle(self, *tenants, **options):
        for tenant in tenants:
            call_command('migrate', database=tenant, **options)
