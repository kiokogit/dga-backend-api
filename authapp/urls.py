from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('account', UsersAccountsManagerViewSet, basename='accounts')

urlpatterns=router.urls