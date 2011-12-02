from django.dispatch import Signal
from django.core.management import call_command

tenant_provider = Signal(providing_args=[])


def generate_public_name(sender, instance, **kwargs):
    if not instance.public_name and instance.name:
        instance.public_name = instance.name
        
def syncdb(sender, instance, created=False, **kwargs):
    if created:
        call_command('syncdb', database=instance.name, interactive=False, verbosity=0)

def migrate(sender, instance, created=False, **kwargs):
    if created:
        call_command('migrate', database=instance.name, interactive=False, verbosity=0)
