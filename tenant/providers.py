import collections
import datetime
import logging
logger = logging.getLogger(__name__)


class DatabaseProvider(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self._tenants = []
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        kt = self.__keytransform__(key)
        from tenant import settings
        
        if kt not in self.store and settings.MULTITENANT_TENANT_DATABASE in self.store:
            if kt not in settings.MULTITENANT_PUBLIC_DATABASES:
                from tenant.models import Tenant
                try:
                    tenant = Tenant.objects.get(name=kt)
                    self[kt] = tenant.settings
                    
                    if settings.MULTITENANT_LIMIT_TENANT_CONNECTIONS:
                        self._tenants.append((kt, datetime.datetime.now()))
                except Tenant.DoesNotExist:
                    pass
                except Tenant.MultipleObjectsReturned:
                    pass
        return self.store[kt]

    def __setitem__(self, key, value):
        kt = self.__keytransform__(key)
        
        if len(self._tenants) > 0:
            from tenant import settings
            if len(self._tenants) >= settings.MULTITENANT_MAX_TENANTS['default']:
                tenant, timestamp = self._tenants.pop(0)
                if tenant and tenant in self.store:
                    logger.debug('Removing {0}({1})...'.format(tenant, timestamp))
                    del self[tenant]
                
        self.store[kt] = value

    def __delitem__(self, key):
        kt = self.__keytransform__(key)
        
        if kt in self.store:
            logger.debug('Closing {0}...'.format(kt))
            from django.db import connections, transaction
            connections[kt].close()
            
            from tenant import settings
            if settings.MULTITENANT_DESTROY_CONNECTION_ON_REMOVE:
                logger.debug('Deleting connection {0}...'.format(kt))
                delattr(connections._connections, kt)
        del self.store[kt]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def __unicode__(self):
        return unicode(self.store)

    def __str__(self):
        return unicode(self)
