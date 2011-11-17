from django.http import Http404

import collections


class DatabaseProvider(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs)) # use the free update to set keys

    def __getitem__(self, key):
        if key != 'default' and key not in self.store and 'default' in self.store:
            from tenant.models import Tenant
            from django.shortcuts import get_object_or_404
            tenant = get_object_or_404(Tenant.objects.using('default'), name=key)
            self[key] = tenant.settings
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
