def tenant(request):
    return {
        'TENANT': getattr(request, 'tenant', None),
    }
