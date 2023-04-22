from django.urls import path

from shared_utils.views import NotificationsViewSet

from .endpoint_utils import GetCountriesData

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('countries', GetCountriesData, basename='countries_data')
router.register('notifications', NotificationsViewSet, basename='notifications')
# router.register('cities', PackagesView, basename='packs')

urlpatterns=router.urls