import json

from collections import OrderedDict

from django.core import serializers
from django.db.models import DecimalField, IntegerField, CharField, ExpressionWrapper, F, Case, Value, When, Q, Sum, Avg, Max, Min, Count

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

def get_regions(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'countries__grants__')
    # Get distinct regions along with the number of total grants and tatal_grants_funded
    #countries__grants__submission_date__gt='2012-10-30'
    regions = Region.objects.filter(**kwargs).distinct(
    ).annotate(
        num_funded=Count(
            Case(
                When(
                    Q(countries__grants__status='Closed')|
                    Q(countries__grants__status='Funded')|
                    Q(countries__grants__status='Completed'), then=1
                ),
                output_field=IntegerField(),
            )
        ),
        num_total=Count(
            Case(
                When(countries__grants__status__isnull=False, then=1),
                output_field=IntegerField(),
            )
        )
    ).annotate(
        win_rate=ExpressionWrapper(F('num_funded')/F('num_total') * 100, DecimalField(decimal_places=2)),
    ).annotate(
        loss_rate=(100 - F('win_rate')),
    ).values('region_id', 'name', 'num_funded', 'num_total', 'win_rate', 'loss_rate')

    series = []
    win_rates_data = []
    loss_rates_data = []
    for r in regions:
        win_rates_data.append( {'y': float(r['win_rate']), 'name': r['name'], 'drilldown': 'win_rate' + str( r['region_id']) } )
        loss_rates_data.append( {'y': float(r['loss_rate']), 'name': r['name'], 'drilldown': 'loss_rate' + str(r['region_id']) } )

    series.append({'name': 'WinRate', 'data': win_rates_data})
    series.append({'name': 'LossRate', 'data': loss_rates_data})
    series_json = json.dumps(series)
    return series_json


def get_countries(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'grants__')
    print(kwargs) #grants__submission_date__gt='2012-10-30'
    countries = Country.objects.filter(**kwargs).distinct(
    ).annotate(
        num_funded=Count(
            Case(
                When(
                    Q(grants__status='Closed')|
                    Q(grants__status='Funded')|
                    Q(grants__status='Completed'), then=1
                ),
                output_field=IntegerField(),
            )
        ),
        num_total=Count(
            Case(
                When(grants__status__isnull=False, then=1),
                output_field=IntegerField(),
            )
        )
    ).annotate(
        win_rate=ExpressionWrapper(F('num_funded')/F('num_total') * 100, DecimalField(decimal_places=2)),
    ).annotate(
        loss_rate=(100 - F('win_rate')),
    ).values('region', 'region__name', 'country_id', 'name', 'num_funded', 'num_total', 'win_rate', 'loss_rate').order_by('region')

    country_drilldown_series_win_rate_data = []
    country_drilldown_series_loss_rate_data = []
    drilldown_series = []
    region = None
    region_name = None

    # get the drilldowns for win_rates per country
    for c in countries:
        if region is not None and region != c['region']:
            drilldown_series.append({'id': 'win_rate' + str(region), 'type': 'column', 'stacking': 'regular', 'name': region_name, 'data': country_drilldown_series_win_rate_data})
            drilldown_series.append({'id': 'loss_rate' + str(region), 'type': 'column', 'stacking': 'regular', 'name': region_name, 'data': country_drilldown_series_loss_rate_data})

            country_drilldown_series_win_rate_data = []
            country_drilldown_series_loss_rate_data = []

        country_drilldown_series_win_rate_data.append( [c['name'], float(c['win_rate']) ])
        country_drilldown_series_loss_rate_data.append( [c['name'], float(c['loss_rate']) ])

        region = c['region']
        region_name = c['region__name']
    drilldown_series.append({'id': 'win_rate' + str(region), 'type': 'column', 'stacking': 'regular', 'name': region_name, 'data': country_drilldown_series_win_rate_data})
    drilldown_series.append({'id': 'loss_rate' + str(region), 'type': 'column', 'stacking': 'regular', 'name': region_name, 'data': country_drilldown_series_loss_rate_data})

    drilldown_series_json = json.dumps(drilldown_series)
    return drilldown_series_json


def get_donor_categories_dataset(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'donors__grants__')
    #print("donor_categories: %s" % kwargs)
    donor_categories = DonorCategory.objects.filter(**kwargs).\
        annotate(drilldown=F('name'), grants_count=Count('donors__grants', distinct=True)).\
        annotate(y=F('grants_count')).values('name', 'drilldown', 'y')
    return list(donor_categories)


def get_donors_dataset(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'grants__')
    #print("donors: %s: " % kwargs)
    donors = Donor.objects.filter(**kwargs).annotate(id=F('category__name'), grants_count=Count('grants', distinct=True)).annotate(y=F('grants_count')).values('id', 'name', 'grants_count', 'y').order_by('id')

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
    return series


def get_grants_dataset(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, '')
    #print("grants: %s" % kwargs)
    grants = Grant.objects.filter(**kwargs).distinct().prefetch_related('donor').order_by('donor')

    series = []
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

    return series


class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(GlobalDashboard, self).get_context_data(**kwargs)
        form = GrantDonorFilterForm()
        context['form'] = form

        donor_categories = get_donor_categories_dataset(self.request.GET)
        donors = get_donors_dataset(self.request.GET)
        grants = get_grants_dataset(self.request.GET)
        series = donors + grants

        context['donor_categories'] = JsonResponse(donor_categories, safe=False).content

        context['donors'] = JsonResponse(series, safe=False).content

        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')
        context['criteria'] = JsonResponse(kwargs, safe=False).content

        # get the win/loss rates by region
        context['regions'] = get_regions(self.request.GET)

        # get all of the win/loss rates by country
        context['regions_drilldown'] = get_countries(self.request.GET)

        return context


class DonorCategoriesView(View):

    def get(self, request, *args, **kwargs):
        donor_categories = get_donor_categories_dataset(self.request.GET)
        donors_list = get_donors_dataset(self.request.GET)
        grants_list = get_grants_dataset(self.request.GET)
        series = donors_list + grants_list

        regions = get_regions(self.request.GET)
        countries = get_countries(self.request.GET)

        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')

        final_dict = {
            'donor_categories': donor_categories,
            'donors': series,
            'regions': regions,
            'countries': countries,
            'criteria': kwargs}
        return JsonResponse(final_dict, safe=False)
