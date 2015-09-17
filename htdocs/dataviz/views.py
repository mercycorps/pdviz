from django.core import serializers
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib import messages

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *

class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        messages.success(self.request, "Hey, This is the Global Dashboard!")
        return super(GlobalDashboard, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Provide context data to the template renderer
        """
        context = super(GlobalDashboard, self).get_context_data(**kwargs)
        data = Donor.objects.filter(grants__isnull=False).annotate(num_grants=Count('grants'))
        serializer = DonorSerializer(data, many=True)
        donors = JSONRenderer().render(serializer.data)
        #donors = serializers.serialize('json', Donor.objects.all(),ensure_ascii=False)
        context['donors'] = donors
        return context