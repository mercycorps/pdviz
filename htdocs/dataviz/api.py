from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from pdviz.utils import *

class DonorViewSet(viewsets.ModelViewSet):
    serializer_class = DonorSerializer
    
    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET)
        num_grants = self.request.GET.get('grants_count', None)
        if num_grants == None:
            return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants'))
        else:
            return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants')).filter(grants_count__gt=num_grants)

    