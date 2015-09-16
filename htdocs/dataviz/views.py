#from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib import messages

class GlobalDashboard(TemplateView):
    template_name='global_dashboard.html'

    def get(self, request, *args, **kwargs):
        messages.success(self.request, "Hey, This is the Global Dashboard!")
        return super(GlobalDashboard, self).get(request, *args, **kwargs)
