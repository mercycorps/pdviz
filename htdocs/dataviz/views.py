from django.core import serializers
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, View

from django.contrib import messages

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *
from .forms import *
from .mixins import *

class CountriesByRegion(JSONResponseMixin, ListView):
    Model = Country

    def get_queryset(self, **kwargs):
        return Country.objects.filter(**self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(CountriesByRegion, self).get_context_data(**kwargs)
        serializer = CountrySerializer(self.get_queryset(), many=True)
        context['serializer'] = serializer
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        #messages.success(self.request, "Hey, This is the Global Dashboard!")
        return super(GlobalDashboard, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Provide context data to the template renderer
        """
        
        # Prefix each key in the URL params with 'grants__' so that Donor's related entries 
        # in Grant table are filtered by following the relationship in reverse fashion
        for key in self.kwargs: 
            self.kwargs['grants__' + key] = self.kwargs.pop(key)

        # Prefix each key in the GET query dictionary with 'grants__' so that Donor's related entries 
        # in Grant table are filtered by following the relationship in reverse fashion
        for k,v in self.request.GET.iteritems():
            self.kwargs['grants__' + k] = v

        # Do not show donors that have no Grants
        self.kwargs['grants__isnull'] = False
        
        # retrieve the context object of the parent view
        context = super(GlobalDashboard, self).get_context_data(**kwargs)
        
        # build the database query
        data = Donor.objects.filter(**self.kwargs).annotate(num_grants=Count('grants'))[:400]
        
        # Use the rest_framework serializer class to serialize model instance to JSON
        serializer = DonorSerializer(data, many=True)
        
        # Encode the serialized object to JSON
        donors = JSONRenderer().render(serializer.data)
        #donors = serializers.serialize('json', Donor.objects.all(),ensure_ascii=False)
        
        # Add the donors JSON encoded String to the context object.
        context['donors'] = donors
        
        # Initiate the form that is to be used in template for filtering the Donor model queryset
        form = GrantDonorFilterForm()
        
        # Add the form to the context object
        context['form'] = form
        
        return context