import math
import locale
from rest_framework import serializers
from .models import *

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class GrantSerializerPlain(serializers.ModelSerializer):
    gait_id = serializers.SerializerMethodField("get_grant_id")
    donor = serializers.SerializerMethodField("get_donor_name")
    amount_usd = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField('get_country_name')
    hq = serializers.SerializerMethodField('get_hqadmin')
    department = serializers.SerializerMethodField('get_department_name')

    class Meta:
        model = Grant
        fields = ("gait_id", "donor", "department", "hq", "country", "title", "amount_usd", "status",  "submission_date")

    def get_grant_id(self, obj):
        return obj.grant_id

    def get_amount_usd(self, obj):
        #return math.trunc(obj.amount_usd)
        return locale.format("%d", obj.amount_usd, grouping=True)

    def get_donor_name(self, obj):
        donor = ""
        if obj.donor:
            donor = obj.donor.name
        return donor

    def get_department_name(self, obj):
        department = ""
        try:
            department = obj.department.name
        except DonorDepartment.DoesNotExist:
            pass
        return department

    def get_country_name(self, obj):
        if obj.countries.count() > 0:
            return obj.countries.all()[0].name #','.join([c.name for c in g.countries.all()])
        else:
            return None

    def get_hqadmin(self, obj):
        if obj.hq_admin == 'Portland':
            return 'PDX'
        elif obj.hq_admin == 'Europe':
            return "EU"
        else:
            return ''


class GrantSerializer(serializers.ModelSerializer):
    gait_id = serializers.SerializerMethodField('get_grant_id')
    win_loss = serializers.SerializerMethodField()
    y = serializers.SerializerMethodField('get_amount_usd')
    id = serializers.SerializerMethodField('get_country_name')
    drilldown = serializers.SerializerMethodField('get_grant_id')
    name = serializers.SerializerMethodField('get_grant_title')
    class Meta:
        model = Grant
        fields = ("gait_id", "name", "id", "win_loss", "drilldown", "y", "start_date", "end_date")

    def get_grant_id(self, obj):
        return obj.grant_id

    def get_amount_usd(self, obj):
        return obj.amount_usd

    def get_grant_title(self, obj):
        return obj.title

    def get_country_name(self, obj):
        if obj.countries.count() > 0:
            return obj.countries.all()[0].name #','.join([c.name for c in g.countries.all()])
        else:
            return None

    def get_win_loss(self, obj):
        return obj.win_loss


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class GrantsByCountrySerializer(serializers.ModelSerializer):
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
        return obj.name


class GrantsByDonorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_donor_id')
    tooltip = serializers.SerializerMethodField()
    data = GrantSerializer(many=True, read_only=True, source="grants")

    class Meta:
        model = Donor
        fields = ("id", "tooltip", "data")

    def get_tooltip(self, obj):
        return {"valueSuffix": " USD", "valuePrefix": "$", "valueDecimals": 2}

    def get_name(self,obj):
        return "Total USD Amount"

    def get_donor_id(self, obj):
        return "d-" + str(obj.donor_id)


class DonorSerializer(serializers.ModelSerializer):
    grants_count = serializers.IntegerField()
    class Meta:
        model = Donor
        fields = '__all__'


class DonorCategorySerializer(serializers.ModelSerializer):
    donors_count = serializers.IntegerField()
    class Meta:
        model = DonorCategory
        fields = '__all__'


class DonorDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorDepartment
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class SubSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        depth = 1
        fields = '__all__'


class MethodologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodology
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
