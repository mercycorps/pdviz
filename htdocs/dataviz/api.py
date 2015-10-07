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
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET)
        num_grants = self.request.GET.get('grants_count', None)
        print(kwargs)
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