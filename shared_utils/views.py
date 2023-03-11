from .utils import format_error

from app import settings

import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authtoken.models import Token


from django.core.mail import send_mail
from django.conf import settings


import jwt
import bcrypt

logger = logging.getLogger(__name__)

class GeneralView(GenericViewSet):
    
    def return_headers(self, request):
        jwt_token = request.headers['JWTAUTH'].split(' ')[1]
        access_token = request.headers['Authorization'].split(' ')[1]
        return {
            'JWTAUTH':jwt_token,
            'Authorization':access_token
        }
    
    def return_serializer_context(self, request):
        headers = self.return_headers(request)
        # decode jwt
        payload = jwt.decode(headers['JWTAUTH'],key=settings.SECRET_KEY, algorithms=['HS256'])
        
        context = {
            "user_id": payload['user_id'],
            "user_type": payload['user_type'],
            "headers":headers
        }
        return context

class SendEmail(GeneralView):

    def sendemail(self, request):
        # django-email-server.py

        res = send_mail(
                subject=request.data.get('subject'),
                message=request.data.get('message'),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=request.data.get('recipients')
        )

        return True




