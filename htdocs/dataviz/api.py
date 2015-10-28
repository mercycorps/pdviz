from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from pdviz.utils import *
"""
data = Grant.objects.filter(submission_date__gt='2010-01-01').extra(select={'fy':'strftime("%%Y", "submissionDate")', 'period': 'case when cast(strftime("%%m", "submissionDate") as integer) between 1 and 6 then "Jan-Jun" else "Jul-Dec" END', 'month': 'strftime("%%m", "submissionDate")'}).values('fy', 'hq_admin', 'period', 'submission_date', 'month')
"""
class DonorViewSet(viewsets.ModelViewSet):
    serializer_class = DonorSerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, prefix='')
        num_grants = self.request.GET.get('grants_count', None)
        if num_grants == None:
            return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants'))
        else:
            return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants')).filter(grants_count__gt=num_grants)
"""
data = Grant.objects.filter(submission_date__gt='2010-01-01').extra(select=
    {   'fy': 'strftime("%%Y", "submissionDate")',
        'period': 'case when cast(strftime("%%m", "submissionDate") as integer) = 0 then "na" else case cast(strftime("%%m", "submissionDate") as integer) between 1 and 6 then "Jan-Jun" else "Jul-Dec" END END',
        'month': 'strftime("%%m", "submissionDate")'})
        .values('fy', 'hq_admin', 'period', 'submission_date', 'month')
"""
#data = Grant.objects.filter(submission_date__gt='2010-01-01').extra(select={'fy': 'strftime("%%Y", "submissionDate")', 'period': 'case when cast(strftime("%%m", "submissionDate") as integer) between 1 and 6 then "Jan-Jun" else case when cast(strftime("%%m", "submissionDate") as integer) between 7 and 12 then "Jul-Dec" else "na" END END', 'month': 'strftime("%%m", "submissionDate")'}).values('fy', 'hq_admin', 'period', 'submission_date', 'month')

#data = Grant.objects.filter(submission_date__gt='2010-01-01').extra(select={'fy': 'strftime("%%Y", "submissionDate")', 'period': 'case when cast(strftime("%%m", "submissionDate") as integer) between 1 and 6 then "Jan-Jun" else case when cast(strftime("%%m", "submissionDate") as integer) between 7 and 12 then "Jul-Dec" else "na" END END', 'month': 'strftime("%%m", "submissionDate")'}).values('fy', 'hq_admin', 'period', 'submission_date', 'month').filter(submission_date__month=0)

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

class DonorCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = DonorCategorySerializer
    #queryset = DonorCategory.objects.all()

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, 'donors__grants__')
        #cs = DonorCategory.objects.filter(donors__grants__submission_date__gte='2011-10-12').values('name', 'donors__donor_id', 'donors__name').annotate(categorycount = Count('donors')).prefetch_related('donors')
        num_grants = 0
        return DonorCategory.objects.filter(**kwargs).annotate(donors_count = Count('donors'), grants_count = Count('donors__grants')).filter(grants_count__gt=num_grants).prefetch_related('donors')
        #dc = DonorCategory.objects.filter(donors__grants__submission_date__gt='2010-01-01').annotate(grants_count=Count('donors__grants')).filter(grants_count__gt=50).prefetch_related('donors')
        #return DonorCategory.objects.filter(**kwargs).annotate(grants_count=Count('donors__grants')).filter(grants_count__gt=num_grants).prefetch_related('donors')
        #for d in dc:
        #    print ("num_grants: %s, num_donors: %s" % (d.grants_count, len(d.donors.all())))
        #
        #
        #
        # http://jsfiddle.net/6LXVQ/2/
        # grants = Grant.objects.filter(submission_date__gte='2014-10-12').values('grant_id', 'submission_date', 'donor__donor_id', 'donor__name', 'donor__category', 'donor__category__name')
        # data = DonorCategory.objects.filter(donors__grants__submission_date__gte='2014-10-12').annotate(donors_count = Count('donors')).prefetch_related('donors')
        # donors = Donor.objects.filter(grants__submission_date__gte='2014-10-12').annotate(grants_count=Count('grants')).filter(grants_count__gte=3).prefetch_related('grants')
        # grants = Grant.objects.filter(submission_date__gte='2014-10-12', donor=855)














