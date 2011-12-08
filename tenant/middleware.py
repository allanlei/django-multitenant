from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404
from django.db import transaction

from tenant.models import Tenant
from tenant.utils import connect_tenant_provider, disconnect_tenant_provider


class TenantMiddleware(object):
    def process_request(self, request):
        request.tenant = None
        name = resolve(request.path).kwargs.get('tenant') or request.GET.get('tenant')
        
        if name:
            tenant = get_object_or_404(Tenant, name=name)
            request.tenant = tenant
            connect_tenant_provider(request, tenant.name)
            
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
        transaction.enter_transaction_management(using=self.get_tenant(request))
        transaction.managed(True, using=self.get_tenant(request))

    def process_exception(self, request, exception):
        """Rolls back the database and leaves transaction management"""
        if transaction.is_dirty(using=self.get_tenant(request)):
            transaction.rollback(using=self.get_tenant(request))
        transaction.leave_transaction_management(using=self.get_tenant(request))

    def process_response(self, request, response):
        """Commits and leaves transaction management."""
        if transaction.is_managed(using=self.get_tenant(request)):
            if transaction.is_dirty(using=self.get_tenant(request)):
                transaction.commit(using=self.get_tenant(request))
            transaction.leave_transaction_management(using=self.get_tenant(request))
        return response
