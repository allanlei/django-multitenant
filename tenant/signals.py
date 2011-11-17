from django.dispatch import Signal
from django.core.management import call_command


request_for_read = Signal(providing_args=[])
request_for_write = Signal(providing_args=[])
request_for_syncdb = Signal(providing_args=[])

tenant_authenticated = Signal(providing_args=['tenant'])
tenant_connected = Signal(providing_args=['tenant'])
tenant_disconnected = Signal(providing_args=['tenant'])

tenant_provider = Signal(providing_args=[])





def generate_public_name(sender, instance, **kwargs):
    if not instance.public_name and instance.name:
        instance.public_name = instance.name
        
def syncdb(sender, instance, created=False, **kwargs):
    if created:
        call_command('syncdb', database=instance.name, interactive=False, migrate_all=True)

def migrate(sender, instance, created=False, **kwargs):
    if created:
        call_command('migrate', database=instance.name, interactive=False)
