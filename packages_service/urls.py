from django.urls import path

from packages_service.ingestion.views import CreateTravelPackage
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('ingestion/', CreateTravelPackage, basename='ingestion_create')

urlpatterns=router.urls