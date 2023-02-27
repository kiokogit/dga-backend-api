from django.urls import path
from .views import *
from .ingestion import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('user', SignUpUser, basename='accounts')
router.register('', LoginUser, basename='login_user')
router.register('roles', UserRolesViewSet, basename='roles' )
router.register('ingestion', IngestAuthData, basename='ingestion' )

# urlpatterns = [
#     path(" ", LoginUser.as_view())
# ]

urlpatterns=router.urls