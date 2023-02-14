from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register('user', SignUpUser, basename='accounts')
router.register('', LoginUser, basename='login_user')

# urlpatterns = [
#     path(" ", LoginUser.as_view())
# ]

urlpatterns=router.urls