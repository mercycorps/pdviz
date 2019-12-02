from urllib.parse import urlencode

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'pdviz/index.html'


class PDVIZLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            # Some places of our code loads HTML directly into a modal via $.load()
            # loading the login page (which uses base.html) blows up a lot of things
            # so avoid this by sending back a simple string instead
            response = HttpResponse('You are not logged in.')
            # Header that jQuery AJAX can look for to see if a request was 302 redirected
            # responseURL could also be used but is not supported in older browsers
            response['Login-Screen'] = 'Login-Screen'
            return response

        return super(PDVIZLoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PDVIZLoginView, self).get_context_data(*args, **kwargs)
        context['okta_url'] = "{base}?{params}".format(
            base=reverse('social:begin', kwargs={'backend': 'saml'}),
            params=urlencode({'idp': 'okta'})
        )
        return context
