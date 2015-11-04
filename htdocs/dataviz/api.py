from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from pdviz.utils import *


class GrantViewSet(viewsets.ModelViewSet):
    serializer_class = GrantSerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, prefix='')
        queryset = Grant.objects.filter(**kwargs)[:50]
        return queryset


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all()
        region_id = self.request.query_params.get('region', None)
        if region_id:
            queryset = queryset.filter(region=region_id)
        return queryset


class DonorViewSet(viewsets.ModelViewSet):
    serializer_class = DonorSerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, prefix='grants__')
        return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants'))


class DonorCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = DonorCategorySerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, 'donors__grants__')
        return DonorCategory.objects.filter(**kwargs).annotate(donors_count = Count('donors'), grants_count = Count('donors__grants')).prefetch_related('donors').order_by('name')


class SectorViewSet(viewsets.ModelViewSet):
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()


class SubSectorViewSet(viewsets.ModelViewSet):
    serializer_class = SubSectorSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = SubSector.objects.all()
        sector_id = self.request.query_params.get('sector', None)
        if sector_id is not None:
            queryset = queryset.filter(sectors=sector_id).prefetch_related('sectors')
        return queryset


class MethodologyViewSet(viewsets.ModelViewSet):
    serializer_class = MethodologySerializer
    queryset = Methodology.objects.all()


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()


