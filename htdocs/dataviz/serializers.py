from rest_framework import serializers
from .models import *


class GrantSerializer(serializers.ModelSerializer):
    gait_id = serializers.SerializerMethodField('get_grant_id')
    y = serializers.SerializerMethodField('get_amount_usd')
    id = serializers.SerializerMethodField('get_country_name')
    name = serializers.SerializerMethodField('get_grant_title')
    class Meta:
        model = Grant
        fields = ("gait_id", "name", "id", "y")

    def get_grant_id(self, obj):
        return obj.grant_id

    def get_amount_usd(self, obj):
        return obj.amount_usd

    def get_grant_title(self, obj):
        return obj.title

    def get_country_name(self, obj):
        return obj.countries.all()[0].name


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
