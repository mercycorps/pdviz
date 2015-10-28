"""pdviz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin

from rest_framework import routers, serializers, viewsets

from .views import *
from dataviz.views import *
from dataviz.api import *

router = routers.DefaultRouter()
router.register('donors', DonorViewSet, base_name='donors')
router.register('countries', CountryViewSet, base_name='countries')
router.register('donorcategories', DonorCategoryViewSet, base_name='donorcategories')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^global/$', GlobalDashboard.as_view(), name='globaldashboard'),
    url(r'^test/$', TestChart.as_view(), name='test_chart'),
    url(r'^grant_id/(?P<grant_id>\d+)/$', GlobalDashboard.as_view(), name='home_category'),
    url(r'^dataviz/countries_by_region/(?P<region>[-\w]+)/$', CountriesByRegion.as_view(), name='cbg'),
    url(r'^z/$', DonorCategoriesView.as_view(), name='z'),
    url(r'^$', HomeView.as_view(), name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)