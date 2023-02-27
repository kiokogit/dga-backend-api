from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('public_accounts', PublicAccountsViewSet, basename='public_profiles')
router.register('general_accounts', GeneralAccountsView, basename='general')

urlpatterns=router.urls