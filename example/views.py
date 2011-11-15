from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections


from models import *
from forms import PlaceForm



class TestView(generic.edit.CreateView):
    template_name = 'test.html'
    form_class = PlaceForm

    def get_success_url(self):
        return self.request.get_full_path()
    
    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context.update({
            'places': Place.objects.all(),
            
            'tenants': {
                'default': Place.objects.using('default').all(),
                'a.com': Place.objects.using('a.com'),
                'b.com': Place.objects.using('b.com'),
                'c.com': Place.objects.using('c.com'),
                'd.com': Place.objects.using('d.com'),
            },
            'connections': connections.all(),
        })
        return context
