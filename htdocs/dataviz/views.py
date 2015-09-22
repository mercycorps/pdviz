from django.core import serializers
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, View

from django.contrib import messages

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from pdviz.utils import *
from .models import *
from .serializers import *
from .forms import *
from .mixins import *
from .api import *


class CountriesByRegion(JSONResponseMixin, ListView):
    model = Country

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
        return super(GlobalDashboard, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Provide context data to the template renderer
        """
        context = super(GlobalDashboard, self).get_context_data(**kwargs)

        #kwargs2 = prepare_related_donor_fields_to_lookup_fields(self.request.GET)
        #data = Donor.objects.annotate(grants_count=Count('grants')).filter(**kwargs2)

        # Use the rest_framework serializer class to serialize model instance to JSON
        #serializer = DonorSerializer(data, many=True)
        
        # Encode the serialized object to JSON
        #donors = JSONRenderer().render(serializer.data)
        #context['donors'] = donors
        

        
        form = GrantDonorFilterForm()
        context['form'] = form
        
        return context