from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404
from django.db import transaction

from tenant.models import Tenant
from tenant.utils import connect_tenant_provider, disconnect_tenant_provider


class TenantMiddleware(object):
    def identify_tenant(self, request):
        name = None
        
        if name is None:
            try:
                name = resolve(request.path).kwargs.get('tenant', None)
            except:
                pass
        if name is None:
            name = request.GET.get('tenant', None)
        return name
        
    def process_request(self, request):
        request.tenant = None
        
        name = self.identify_tenant(request)
        if name:
            tenant = get_object_or_404(Tenant, name=name)
            request.tenant = tenant
            connect_tenant_provider(request, tenant.ident)
        return None
        
    def process_response(self, request, response):
        disconnect_tenant_provider(request)
        request.tenant = None
        return response


class TransactionMiddleware(object):
    def get_tenant(self, request):
        tenant = getattr(request, 'tenant', None)
        if tenant:
            return tenant.ident
        
    def process_request(self, request):
        """Enters transaction management"""
        db = self.get_tenant(request)
        if db:
            transaction.enter_transaction_management(using=db)
            transaction.managed(True, using=db)

    def process_exception(self, request, exception):
        """Rolls back the database and leaves transaction management"""
        db = self.get_tenant(request)
        if db:
            if transaction.is_dirty(using=db):
                transaction.rollback(using=db)

            if transaction.is_managed(using=db):
                transaction.leave_transaction_management(using=db)

    def process_response(self, request, response):
        """Commits and leaves transaction management."""
        db = self.get_tenant(request)
        if db:
            if transaction.is_managed(using=db):
                if transaction.is_dirty(using=db):
                    transaction.commit(using=db)
                transaction.leave_transaction_management(using=db)
        return response
