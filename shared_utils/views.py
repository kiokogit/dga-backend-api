import logging
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from packages_service.views import GeneralView

from shared_utils.models import NotificationsModel
from shared_utils.serializers import NotificationsListSerializer

logger = logging.getLogger(__name__)


class SendEmail(GeneralView):

    def sendemail(self, request):
        # django-email-server.py

        res = send_mail(
                subject=request.data.get('subject'),
                message=request.data.get('message'),
                from_email=settings.EMAIL_HOST_USER, #type:ignore
                recipient_list=request.data.get('recipients')
        )

        #send also notification

        return True

class NotificationsViewSet(ListModelMixin, GeneralView):
    queryset = NotificationsModel.objects.all()
    serializer_class = NotificationsListSerializer
    ordering_fields = ['-date_created']
    ordering = ['-date_created']
    model = NotificationsModel
    permission_classes=(AllowAny,)


    # def get_queryset(self):
    #     receiver = self.get_logged_in_user(self.request)
    #     if receiver:
    #         return self.queryset.filter(receiver=receiver)
    #     return super().get_queryset()
    
    
    @action(methods=['GET'], detail=False)
    def get_user_notifications(self, request):

        pass


