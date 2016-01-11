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


class CountrySerializer(serializers.ModelSerializer):
    data = GrantSerializer(many=True, read_only=True, source="grants")
    type = serializers.SerializerMethodField()
    dataLabels = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField('get_country_name')
    tooltip = serializers.SerializerMethodField()
    stacking = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "iso2","name", "region", "type", "stacking", "dataLabels", "tooltip", "data")

    def get_type(self, obj):
        return "column"

    def get_dataLabels(self, obj):
        return {'enabled': True, 'format': '{point.y:,.0f}'}

    def get_country_name(self, obj):
        return obj.name

    def get_tooltip(self, obj):
        return {"valueSuffix": " USD", "valuePrefix": "$", "valueDecimals": 2}

    def get_stacking(self, obj):
        return "regular"

    def get_name(self,obj):
        return "GRANTS"


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
