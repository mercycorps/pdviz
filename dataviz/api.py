from operator import and_, or_
from functools import reduce
from django.db.models import Q

from rest_framework import viewsets, pagination
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *
from pdviz.utils import *

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GrantViewSet(viewsets.ModelViewSet):
    serializer_class = GrantSerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, prefix='')
        queryset = Grant.objects.filter(**kwargs)[:50]
        return queryset


class GrantsByCountryViewSet(viewsets.ModelViewSet):
    serializer_class = GrantsByCountrySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Country.objects.all()
        region_ids = self.request.query_params.get('region', None)
        if region_ids:
            region_list = region_ids.split(',')
            queryset = queryset.filter( reduce(or_, [Q(region=r) for r in region_list]) )
        return queryset


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    pagination.PageNumberPagination.page_size = 100

    def get_queryset(self):
        queryset = Country.objects.all()
        region_ids = self.request.query_params.get('region', None)
        if region_ids:
            region_list = region_ids.split(',')
            queryset = queryset.filter( reduce(or_, [Q(region=r) for r in region_list]) )
        return queryset


class DonorViewSet(viewsets.ModelViewSet):
    serializer_class = DonorSerializer

    def get_queryset(self):
        kwargs = prepare_related_donor_fields_to_lookup_fields(self.request.GET, prefix='grants__')
        return Donor.objects.filter(**kwargs).annotate(grants_count=Count('grants'))


class DonorDepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DonorDepartmentSerializer

    def get_queryset(self):
        queryset = DonorDepartment.objects.all()
        donor_ids = self.request.query_params.get('donor', None)
        if donor_ids:
            donor_list = donor_ids.split(',')
            queryset = queryset.filter(donor__in=donor_list)
        return queryset


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


