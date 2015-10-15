from rest_framework import serializers
from .models import *


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant


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