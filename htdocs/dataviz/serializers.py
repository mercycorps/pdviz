from rest_framework import serializers
from .models import *


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        depth = 1


class DonorSerializer(serializers.ModelSerializer):
    grants_count = serializers.IntegerField()
    class Meta:
        model = Donor


class DonorCategorySerializer(serializers.ModelSerializer):
    donors_count = serializers.IntegerField()
    class Meta:
        model = DonorCategory


class DonorDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorDepartment


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector


class SubSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        depth = 1


class MethodologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodology


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
