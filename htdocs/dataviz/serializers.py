
from rest_framework import serializers

from .models import *

class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant

class DonorSerializer(serializers.ModelSerializer):
    num_grants = serializers.IntegerField()
    class Meta:
        model = Donor

class DonorDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorDepartment