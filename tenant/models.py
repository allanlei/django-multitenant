from django.db import models
from django.conf import settings

from tenant.utils import parse_connection_string
from tenant.utils import connect_tenant_provider, disconnect_tenant_provider
from tenant import settings as tenant_settings


class Tenant(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    public_name = models.CharField(max_length=256)

    @property
    def ident(self):
        return self.name
        
    @property
    def settings(self):
        return settings.DATABASES[tenant_settings.MULTITENANT_TENANT_DATABASE].copy()
    
    def __unicode__(self):
        return self.public_name
    
        

from django.db.models.signals import pre_save, post_save, post_init, post_delete
from signals import generate_public_name, syncdb, migrate


pre_save.connect(generate_public_name, sender=Tenant)

#if tenant_settings.MULTITENANT_SYNCDB_ONCREATE:
#    post_save.connect(syncdb, sender=Tenant)
#    
#if tenant_settings.MULTITENANT_MIGRATE_ONCREATE:
#    post_save.connect(migrate, sender=Tenant)
