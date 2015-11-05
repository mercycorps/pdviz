from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib import messages

class HomeView(TemplateView):
    template_name='index.html'

    def get(self, request, *args, **kwargs):
        #messages.success(self.request, "Hey, I'm Okay.")
        return super(HomeView, self).get(request, *args, **kwargs)