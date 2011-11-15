import django.dispatch


request_for_read = django.dispatch.Signal(providing_args=[])
request_for_write = django.dispatch.Signal(providing_args=[])
request_for_syncdb = django.dispatch.Signal(providing_args=[])
