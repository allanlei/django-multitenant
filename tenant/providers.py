import collections


class DatabaseProvider(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        from tenant import settings
        if key not in self.store and settings.MULTITENANT_TENANT_DATABASE in self.store:
            if key not in settings.MULTITENANT_PUBLIC_DATABASES:
                from tenant.models import Tenant
                try:
                    tenant = Tenant.objects.get(name=key)
                    self[key] = tenant.settings
                except Tenant.DoesNotExist, Tenant.MultipleObjectsReturned:
                    pass
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

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
