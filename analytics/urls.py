from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('packages', PackagesAnalytics, basename='packages')
router.register('users', UsersAnalytics, basename='users')


urlpatterns=router.urls