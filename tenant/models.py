from django.db import models
from django.conf import settings

from tenant.utils import parse_connection_string


class Tenant(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    public_name = models.CharField(max_length=256)
    connection = models.TextField(blank=True)     #Database connection string

    @property
    def settings(self):
        try:
            return parse_connection_string(self.connection)
        except:
            pass
        return settings.DATABASES['default'].copy()
    
    def __unicode__(self):
        return self.public_name
    
    @property
    def ident(self):
        return self.name

from django.db.models.signals import pre_save, post_save, post_init
from signals import generate_public_name, syncdb, migrate

pre_save.connect(generate_public_name, sender=Tenant)
post_save.connect(syncdb, sender=Tenant)    #migrate_all=True
#post_save.connect(migrate, sender=Tenant)
