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
from django.urls import include, path
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache, cache_page
from django.contrib import admin
from django.contrib.auth.views import LoginView

from rest_framework import routers, serializers, viewsets
from rest_framework_swagger.views import get_swagger_view


from .views import *
from dataviz.views import *
from dataviz.api import *

import feedback

swagger_schema_view = get_swagger_view(title='PDViz')

router = routers.DefaultRouter()
router.register('grants', GrantViewSet, base_name='grants')
router.register('grants_by_country', GrantsByCountryViewSet, base_name='grants_by_country')
router.register('donors', DonorViewSet, base_name='donors')
router.register('countries', CountryViewSet, base_name='countries')
router.register('donorcategories', DonorCategoryViewSet, base_name='donorcategories')
router.register('donordepartments', DonorDepartmentViewSet, base_name='donordepartments')
router.register('sector', SectorViewSet, base_name='sectors')
router.register('subsector', SubSectorViewSet, base_name='subsectors')
router.register('methodologies', MethodologyViewSet, base_name='methodologies')
router.register('themes', ThemeViewSet, base_name='themes')


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/v1/', include(router.urls)),
    path(r'api/docs/', swagger_schema_view),
    path(r'login/', LoginView.as_view(), name='login'),
    # path('', include('django.contrib.auth.urls')),
    path(r'', HomeView.as_view(), name='home'),
    path(r'global_dashboard/', cache_page(60*60*12)(GlobalDashboard.as_view()), name='global_dashboard'),
    path(r'global_dashboard_data/', cache_page(60*60*12)(GlobalDashboardData.as_view()), name='global_dashboard_data'),
    #url(r'^dataviz/countries_by_region/(?P<region>[-\w]+)/$', CountriesByRegion.as_view(), name='cbg'),
    # TODO:  add back feedback module
    # path(r'^feedback/', feedback.urls),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
