#from django.views import generic
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
#from django.db import connections
#from django.conf import settings

#from django.utils import simplejson as json


#from models import *
#from forms import PlaceForm

#import random
#import time


#tenants = settings.DATABASES.keys()

#def create_objects():
#    amount = random.randint(0, 10)
#    for i in range(amount):
#        tenant = random.choice(tenants)
##        print 'create for %s' % tenant
#        Place.objects.using(tenant).create(name='%s%s' % (tenant.split('.')[0], i))

#def random_sleep(ident):
#    pass
##    print 'Sleeping %s...' % id(ident)
##    time.sleep(random.random() * 4)
##    print '\tWoke up %s' % id(ident)
#        
#class TestView(generic.edit.CreateView):
#    template_name = 'test.html'
#    form_class = PlaceForm

#    def get(self, *args, **kwargs):
#        create_objects()
#            
#        random_sleep(self.request)
#        create_objects()
#        if self.request.is_ajax():
#            create_objects()
#            data = list(Place.objects.values())
#            create_objects()
#            data = []
##            data = [{
##                'id': 1,
##                'name': 'a0',
##            }]
#            return HttpResponse(json.dumps(data), mimetype='application/json')
#        create_objects()
#        return super(TestView, self).get(*args, **kwargs)

#    def get_success_url(self):
#        return self.request.get_full_path()
#    
#    def get_context_data(self, **kwargs):
#        context = super(TestView, self).get_context_data(**kwargs)
#        context.update({
#            'places': Place.objects.all(),
#            'tenants': dict([(tenant, Place.objects.using(tenant)) for tenant in tenants]),
#            'connections': connections.all(),
#        })
#        return context
