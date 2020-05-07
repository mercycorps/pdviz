from rest_framework import routers
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache, cache_page
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from .views import PDVIZLoginView, HomeView
from dataviz.api import *
from dataviz.views import GlobalDashboard, GlobalDashboardData


router = routers.DefaultRouter()
router.register('grants', GrantViewSet, basename='grants')
router.register('grants_by_country', GrantsByCountryViewSet, basename='grants_by_country')
router.register('donors', DonorViewSet, basename='donors')
router.register('countries', CountryViewSet, basename='countries')
router.register('donorcategories', DonorCategoryViewSet, basename='donorcategories')
router.register('donordepartments', DonorDepartmentViewSet, basename='donordepartments')
router.register('sector', SectorViewSet, basename='sectors')
router.register('subsector', SubSectorViewSet, basename='subsectors')
router.register('methodologies', MethodologyViewSet, basename='methodologies')
router.register('themes', ThemeViewSet, basename='themes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('accounts/login/', PDVIZLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', include('social_django.urls', namespace='social')),
    # path('', include('django.contrib.auth.urls')),
    re_path('^$', HomeView.as_view(), name='home'),
    path('global_dashboard/', cache_page(60*60*12)(GlobalDashboard.as_view()), name='global_dashboard'),
    path(r'global_dashboard_data/', cache_page(60*60*12)(GlobalDashboardData.as_view()), name='global_dashboard_data'),
    #url(r'^dataviz/countries_by_region/(?P<region>[-\w]+)/$', CountriesByRegion.as_view(), name='cbg'),
    # TODO:  add back feedback module?
    # path(r'^feedback/', include(feedback.urls)),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
