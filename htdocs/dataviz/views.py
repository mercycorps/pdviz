import json
import time

from collections import OrderedDict

from django.core import serializers
from django.db.models import DecimalField, FloatField, IntegerField, CharField, ExpressionWrapper, F, Case, Value, When, Q, Sum, Avg, Max, Min, Count
from django.db.models.functions import Coalesce
from django.db.models.expressions import RawSQL

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
    """
    Win/Loss rate of grants by region.
    """
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'countries__grants__')
    # Get distinct regions along with the number of total grants and total_grants_funded
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
                When(
                    Q(countries__grants__status__isnull = False)&
                    ~Q(countries__grants__status = 'Concept')&
                    ~Q(countries__grants__status = 'Development')&
                    ~Q(countries__grants__status = 'No-Response')&
                    ~Q(countries__grants__status = 'Pending'), then=1
                ),
                output_field=IntegerField(),
            )
        ),
        amt_funded=Sum(
            Case(
                When(
                    Q(countries__grants__status='Closed')|
                    Q(countries__grants__status='Funded')|
                    Q(countries__grants__status='Completed'), then='countries__grants__amount_usd'
                ),
                output_field=FloatField(),
            )
        ) / 1000000,
        amt_total=Sum(
            Case(
                When(
                    Q(countries__grants__status__isnull = False)&
                    ~Q(countries__grants__status = 'Concept')&
                    ~Q(countries__grants__status = 'Development')&
                    ~Q(countries__grants__status = 'No-Response')&
                    ~Q(countries__grants__status = 'Pending'), then='countries__grants__amount_usd'
                ),
                output_field=FloatField(),
            )
        ) / 1000000,
    ).annotate(
        win_rate=ExpressionWrapper(F('num_funded')/F('num_total') * 100, DecimalField(decimal_places=2)),
    ).annotate(
        loss_rate=(100 - F('win_rate')),
    ).values('region_id', 'name', 'num_funded', 'num_total', 'amt_funded', 'amt_total', 'win_rate', 'loss_rate')

    win_rates_data = []
    loss_rates_data = []
    win_amts_data = []
    loss_amts_data = []
    overallWins = 0
    overallApplications = 0
    overallAmountWon = 0
    overallAmountTried = 0
    for r in regions:
        overallWins += r['num_funded']
        overallApplications += r['num_total']
        overallAmountWon += r['amt_funded'] or 0
        overallAmountTried += r['amt_total'] or 0
        win_rate = r['win_rate']
        loss_rate = r['loss_rate']
        wins = r['num_funded']
        losses = r['num_total'] - wins
        winAmts = r['amt_funded'] or 0
        lossAmts = (r['amt_total'] or 0) - winAmts
        # win_rates_data.append( {'y': float(win_rate if win_rate else 0), 'name': r['name'], 'drilldown': 'wr' + str( r['region_id'])+"-ar"+str( r['region_id']) } )
        # loss_rates_data.append( {'y': float(loss_rate if loss_rate else 0), 'name': r['name'], 'drilldown': 'lr' + str(r['region_id'])+"-ar"+str( r['region_id']) } )
        win_rates_data.append( {'y': wins, 'name': r['name'], 'drilldown': 'wr' + str( r['region_id'])+"-ar"+str( r['region_id']) } )
        loss_rates_data.append( {'y': losses, 'name': r['name'], 'drilldown': 'lr' + str(r['region_id'])+"-ar"+str( r['region_id']) } )
        win_amts_data.append( {'y': winAmts, 'name': r['name'], 'drilldown': 'wr' + str( r['region_id'])+"-ar"+str( r['region_id']) } )
        loss_amts_data.append( {'y': lossAmts, 'name': r['name'], 'drilldown': 'lr' + str(r['region_id'])+"-ar"+str( r['region_id']) } )

    try:
        overallWinRate = float(overallWins)/float(overallApplications)
    except ZeroDivisionError:
        overallWinRate = 0

    series = [{'name': 'WinRate', 'data': win_rates_data}]
    series.append({'name': 'LossRate', 'data': loss_rates_data})

    seriesAmts = [{'name': 'WinAmts', 'data': win_amts_data}]
    seriesAmts.append({'name': 'LossAmts', 'data': loss_amts_data})


    return series, seriesAmts, overallWins, overallApplications, overallAmountWon, overallAmountTried


def get_countries(criteria):
    """
    Get a list of countries along with grants grouped by won and lost
    """
    kwargs = prepare_related_donor_fields_to_lookup_fields(criteria, 'grants__')
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
                When(
                    Q(grants__status__isnull=False) &
                    ~Q(grants__status="Concept") &
                    ~Q(grants__status="Development") &
                    ~Q(grants__status="No-Response") &
                    ~Q(grants__status="Pending"), then=1,
                ),
                output_field=IntegerField(),
            )
        ),
        amt_funded=Sum(
            Case(
                When(
                    Q(grants__status='Closed')|
                    Q(grants__status='Funded')|
                    Q(grants__status='Completed'), then='grants__amount_usd'
                ),
                output_field=IntegerField(),
            )
        ) / 1000000,
        amt_total=Sum(
            Case(
                When(
                    Q(grants__status__isnull=False) &
                    ~Q(grants__status="Concept") &
                    ~Q(grants__status="Development") &
                    ~Q(grants__status="No-Response") &
                    ~Q(grants__status="Pending"), then='grants__amount_usd'
                ),
                output_field=IntegerField(),
            )
        ) / 1000000
    ).annotate(
        win_rate=ExpressionWrapper(F('num_funded')/F('num_total') * 100, DecimalField(decimal_places=2)),
    ).annotate(
        loss_rate=(100 - F('win_rate')),
    ).annotate(
        win_amt_rate=ExpressionWrapper(F('amt_funded')/F('amt_total') * 100, DecimalField(decimal_places=2)),
    ).annotate(
        loss_amt_rate=(100 - F('win_rate')),).values('region', 'region__name', 'country_id', 'name', 'iso2', 'num_funded', 'num_total', 'amt_funded', 'amt_total', 'win_rate', 'loss_rate', 'win_amt_rate', 'loss_amt_rate').order_by('region')

    countries_per_region_winrate_drilldown = []
    countries_per_region_lossrate_drilldown = []
    countries_per_region_winamt_drilldown = []
    countries_per_region_lossamt_drilldown = []

    drilldown_win_series = []
    drilldown_loss_series = []
    drilldown_winamt_series = []
    drilldown_lossamt_series = []

    grants_win_series = []
    grants_loss_series = []
    grants_winamt_series = []
    grants_lossamt_series = []

    region = None
    region_name = None
    cids = None

    # get the drilldowns for win_rates per country
    for c in countries:
        for k in kwargs:
            if k == "grants__countries__country_id__in":
                cids = [int(x) for x in kwargs[k]]

        if cids is not None and int(c['country_id']) not in cids:
            continue

        serializer_lost_grants = None
        serializer_won_grants = None
        grants_won = None
        grants_lost = None

        if region is not None and region != c['region']:
            drilldown_win_series.append({'name': "WIN-RATE - " + region_name, 'id': 'wr' + str(region) +"-ar"+str(region), 'stacking': '', 'data': countries_per_region_winrate_drilldown})
            drilldown_loss_series.append({'name': "LOSS-RATE - " + region_name, 'id': 'lr' + str(region)+"-ar"+str(region), 'stacking': '', 'data': countries_per_region_lossrate_drilldown})
            drilldown_winamt_series.append({'name': "WIN-RATE - " + region_name, 'id': 'wr' + str(region) +"-ar"+str(region), 'stacking': '', 'data': countries_per_region_winamt_drilldown})
            drilldown_lossamt_series.append({'name': "LOSS-RATE - " + region_name, 'id': 'lr' + str(region)+"-ar"+str(region), 'stacking': '', 'data': countries_per_region_lossamt_drilldown})

            countries_per_region_winrate_drilldown = []
            countries_per_region_lossrate_drilldown = []
            countries_per_region_winamt_drilldown = []
            countries_per_region_lossamt_drilldown = []

        wins = c['num_funded'] or 0
        losses = (c['num_total'] or 0) - wins
        print 'funded, total', c['amt_funded'], c['amt_total']
        win_amts = c['amt_funded'] or 0
        loss_amts = (c['amt_total'] or 0) - win_amts
        print 'loss_amts', loss_amts

        # countries_per_region_winrate_drilldown.append({"name": c["name"], "y": float(win_rate if win_rate else 0), "drilldown": "wc"+str(c["country_id"])+"-ac"+ str(c["country_id"])})
        # countries_per_region_lossrate_drilldown.append({"name": c["name"], "y": float(loss_rate if loss_rate else 0), "drilldown": "lc"+str(c["country_id"])+"-ac"+ str(c["country_id"]) })
        countries_per_region_winrate_drilldown.append({"name": c["name"], "y": wins, "drilldown": "wc"+str(c["country_id"])+"-ac"+ str(c["country_id"])})
        countries_per_region_lossrate_drilldown.append({"name": c["name"], "y": losses, "drilldown": "lc"+str(c["country_id"])+"-ac"+ str(c["country_id"]) })
        countries_per_region_winamt_drilldown.append({"name": c["name"], "y": win_amts, "drilldown": "wc"+str(c["country_id"])+"-ac"+ str(c["country_id"])})
        countries_per_region_lossamt_drilldown.append({"name": c["name"], "y": loss_amts, "drilldown": "lc"+str(c["country_id"])+"-ac"+ str(c["country_id"]) })

        kwargs = prepare_related_donor_fields_to_lookup_fields(criteria, '')

        grants_won = Grant.won_grants.filter(countries__country_id=c['country_id'], **kwargs).annotate(win_loss=RawSQL('SELECT "won"', ()))
        serializer_won_grants = GrantSerializer(grants_won, many=True)
        grants_win_series.append({
            "name": c['name'] + " WON Grants",
            "id": "wc" + str(c["country_id"])+"-ac"+ str(c["country_id"]),
            "type": "column",
            #"colorByPoint": True,
            "stacking": "",
            "tooltip": {"valueSuffix": " USD", "valuePrefix": "$", "valueDecimals": 2, "pointFormat": '{series.name}: <b>{point.y}</b><br/>',},
            "dataLabels": {'enabled': False, 'format': '{point.y:,.0f}'},
            "data": serializer_won_grants.data,
        })
        grants_lost = Grant.lost_grants.filter(countries__country_id=c['country_id'], **kwargs).annotate(win_loss=RawSQL('SELECT "loss"', ()))
        serializer_lost_grants = GrantSerializer(grants_lost, many=True)
        grants_loss_series.append({
            "name": c['name'] + " LOST Grants",
            "id": "lc" + str(c["country_id"])+"-ac"+ str(c["country_id"]),
            "type": "column",
            #"colorByPoint": True,
            "stacking": "",
            "tooltip": {"valueSuffix": " USD", "valuePrefix": "$", "valueDecimals": 2, "pointFormat": '{series.name}: <b>{point.y}</b><br/>'},
            "dataLabels": {'enabled': False, 'format': '{point.y:,.0f}'},
            "data": serializer_lost_grants.data,
        })

        region = c['region']
        region_name = c['region__name']

    drilldown_win_series.append({'name': region_name, 'id': 'wr' + str(region)+"-ar"+str(region), 'type': 'column', 'stacking': '', 'data': countries_per_region_winrate_drilldown})
    drilldown_loss_series.append({'name': region_name, 'id': 'lr' + str(region)+"-ar"+str(region), 'type': 'column', 'stacking': '', 'data': countries_per_region_lossrate_drilldown})
    drilldown_winamt_series.append({'name': region_name, 'id': 'wr' + str(region)+"-ar"+str(region), 'type': 'column', 'stacking': '', 'data': countries_per_region_winamt_drilldown})
    drilldown_lossamt_series.append({'name': region_name, 'id': 'lr' + str(region)+"-ar"+str(region), 'type': 'column', 'stacking': '', 'data': countries_per_region_lossamt_drilldown})

    print 'drill wins', json.dumps(drilldown_win_series)[:200]
    print 'drill losses', json.dumps(drilldown_loss_series)[:200]
    print 'drill win amts', json.dumps(drilldown_winamt_series)[:200]
    print 'drill loss amts', json.dumps(drilldown_lossamt_series)[:200]
    drilldown_rate_series = drilldown_win_series + drilldown_loss_series + grants_win_series + grants_loss_series
    drilldown_amt_series = drilldown_winamt_series + drilldown_lossamt_series + grants_win_series + grants_loss_series
    return drilldown_rate_series, drilldown_amt_series


def get_donor_categories_dataset(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'donors__grants__')
    #print("donor_categories: %s" % kwargs)
    donor_categories = DonorCategory.objects.filter(**kwargs).annotate(drilldown=F('name'), grants_count=Count('donors__grants', distinct=True)).annotate(y=F('grants_count')).values('name', 'drilldown', 'y')
    return list(donor_categories)


def get_donors_dataset(kwargs):
    kwargs = prepare_related_donor_fields_to_lookup_fields(kwargs, 'grants__')
    #print("donors: %s: " % kwargs)
    donors = Donor.objects.filter(**kwargs).annotate(id=F('category__name'), grants_count=Count('grants', distinct=True)).annotate(y=F('grants_count')).values('id', 'name', 'donor_id', 'grants_count', 'y').order_by('id')

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
        bar['drilldown'] = "d-" + str(d['donor_id']) # set the name of the drilldown graph for this bar
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
        id = "d-" + str(g.donor.donor_id)
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
        bar['submitted'] = g.submission_date.strftime("%Y-%m-%d") if g.submission_date else ""
        bar['start_date'] = g.start_date.strftime("%Y-%m-%d") if g.start_date else ""
        bar['end_date'] = g.end_date.strftime("%Y-%m-%d") if g.end_date else ""
        data.append(bar)
        bar = OrderedDict()
    graph = {}
    graph['id'] = id
    graph['name'] = graph_name
    graph['data'] = data
    graph['tooltip'] = tooltip
    series.append(graph)

    return {"series": series, "grants": grants}


class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(GlobalDashboard, self).get_context_data(**kwargs)
        form = GrantDonorFilterForm()
        context['form'] = form

        donor_categories = get_donor_categories_dataset(self.request.GET)
        donors = get_donors_dataset(self.request.GET)
        grants = get_grants_dataset(self.request.GET)
        grants_table_serializer = GrantSerializerPlain(grants.pop("grants"), many=True)
        series = donors + grants.pop("series")

        context['donor_categories'] = json.dumps(donor_categories)
        context['donors'] = json.dumps(series)
        context['grants'] = json.dumps(grants_table_serializer.data)

        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')
        context['criteria'] = json.dumps(kwargs)

        # get the win/loss rates by region
        regions, regionAmts, overallWins, overallApplications, overallAmountWon, overallAmountTried = get_regions(self.request.GET)
        context['regions'] = json.dumps(regions)
        context['regionAmts'] = json.dumps(regionAmts)
        context['overallWins'] = overallWins
        context['overallApplications'] = overallApplications
        context['overallAmountWon'] = overallAmountWon
        context['overallAmountTried'] = overallAmountTried

        # get all of the win/loss rates by country
        countries_rates, countries_amts = get_countries(self.request.GET)
        context['regions_drilldown'] = json.dumps(countries_rates)
        context['regions_amt_drilldown'] = json.dumps(countries_amts)
        return context


class GlobalDashboardData(View):

    def get(self, request, *args, **kwargs):
        #print(self.request.GET)
        donor_categories = get_donor_categories_dataset(self.request.GET)
        donors_list = get_donors_dataset(self.request.GET)
        grants_list = get_grants_dataset(self.request.GET)
        grants_table_serializer = GrantSerializerPlain(grants_list.pop("grants"), many=True)
        series = donors_list + grants_list.pop("series")

        regions, regionAmts, overallWins, overallApplications, overallAmountWon, overallAmountTried = get_regions(self.request.GET)
        # regions, overallWins, overallApplications = get_regions(self.request.GET)
        countries_rate, countries_amts = get_countries(self.request.GET)
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, '')

        final_dict = {
            'donor_categories': donor_categories,
            'donors': series,
            'regions': regions,
            'regionAmts': regionAmts,
            'overallWins': overallWins,
            'overallApplications': overallApplications,
            'overallAmountWon': overallAmountWon,
            'overallAmountTried': overallAmountTried,
            'countries': countries_rate,
            'countries_amts': countries_amts,
            'grants': grants_table_serializer.data,
            'criteria': kwargs}
        return JsonResponse(final_dict, safe=False)
