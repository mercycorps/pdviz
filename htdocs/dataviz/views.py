from collections import OrderedDict

from django.core import serializers
from django.db.models import Avg, Max, Min, Count, F

from django.http import HttpResponse, JsonResponse
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

"""
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
"""


class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'

    def get(self, request, *args, **kwargs):
        return super(GlobalDashboard, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Provide context data to the template renderer
        """
        context = super(GlobalDashboard, self).get_context_data(**kwargs)
        form = GrantDonorFilterForm()
        context['form'] = form
        return context


class DonorCategoriesView(View):

    def get_donor_categories_dataset(self, kwargs):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, 'donors__grants__')
        #print("donor_categories: %s" % kwargs)
        donor_categories = DonorCategory.objects.filter(**kwargs).annotate(drilldown=F('name'), donors_count=Count('donors', distinct=True)).annotate(y=F('donors_count')).values('name', 'drilldown', 'donors_count', 'y')
        return list(donor_categories)

    def get_donors_dataset(self, kwargs):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, 'grants__')
        #print("donors: %s: " % kwargs)
        donors = Donor.objects.filter(**kwargs).annotate(id=F('category__name'), grants_count=Count('grants', distinct=True)).annotate(y=F('grants_count')).values('id', 'name', 'grants_count', 'y').order_by('id')
        return donors

    def get_grants_dataset(self, kwargs):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')
        #print("grants: %s" % kwargs)
        grants = Grant.objects.filter(**kwargs).distinct().prefetch_related('donor').order_by('donor')
        return grants

    def get(self, request, *args, **kwargs):
        donor_categories = self.get_donor_categories_dataset(kwargs)
        donors = self.get_donors_dataset(kwargs)
        grants = self.get_grants_dataset(kwargs)

        series = []
        graph = {}
        prev_id = None
        id = None
        graph_name = '# Grants Per Donor'
        data = []
        bar = {}
        bar_name = None

        """
        bar = represent a donor
        data = represents a set of donors that belong to the same donor category
        y = represents the num of donors that a category has
        """
        for d in donors:
            id = d['id'] # donor_category setting the id of the graph, which corresponds to the parent graph drilldown attribute
            if prev_id != id:
                if data:
                    graph['id'] = prev_id
                    graph['name'] = graph_name
                    graph['data'] = data
                    series.append(graph)
                    data = [] # Initialize the data list for the new graph
                    graph = {} # initialize a new graph
                prev_id = id
            bar_name = d['name'] # assign the barname to a variable for reuse
            bar['name'] = bar_name # set the name of the bar on the X-axis
            bar['y'] = d['y'] # set the bar's value for the Y-axis
            bar['grants_count'] = d['grants_count'] # set the bar's value for the Y-axis
            bar['drilldown'] = d['name'] # set the name of the drilldown graph for this bar
            data.append(bar) # append the bar to the graph's data list
            bar = {} # Initialize a new bar

        graph = {}
        graph['id'] = id
        graph['name'] = graph_name
        graph['data'] = data
        series.append(graph)


        prev_id  = None
        id = None
        graph = {}
        graph_name = 'Total USD Amount'
        data = []
        bar = OrderedDict()
        tooltip = {'valuePrefix': '$', 'valueSuffix': ' USD', 'valueDecimals': 2}
        for g in grants:
            try:
                if g.donor == None: continue
            except Exception as e:
                continue
            id = g.donor.name
            if prev_id != id:
                if data:
                    graph['id'] = prev_id
                    graph['name'] = graph_name
                    graph['data'] = data
                    graph['tooltip'] = tooltip
                    series.append(graph)
                    data = []
                    graph = {}
                prev_id = id
            bar['gait_id'] = g.grant_id
            bar['country'] = ','.join([c.name for c in g.countries.all()])
            bar['name'] = g.title
            bar['drilldown'] = g.grant_id
            bar['y'] = g.amount_usd
            bar['amount_usd'] = g.amount_usd
            bar['start_date'] = g.start_date
            bar['end_date'] = g.end_date
            data.append(bar)
            bar = OrderedDict()
        graph = {}
        graph['id'] = id
        graph['name'] = graph_name
        graph['data'] = data
        graph['tooltip'] = tooltip
        series.append(graph)
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')

        final_dict = {'donor_categories': donor_categories, 'donors': series, 'criteria': kwargs}
        return JsonResponse(final_dict, safe=False)
