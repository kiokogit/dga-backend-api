
from authapp.authentication import EmptyAuthenticationClass
from shared_utils.utils import format_error
from .models import UserModel
from . import serializers
from app import settings

import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authtoken.models import Token


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
    
    @staticmethod
    def get_user_by_email(email, user_type):
        user = UserModel.objects.filter(email=email, user_type=user_type)
        if user.exists():
            return True, user.first()
        else:
            return False, None

class IngestAuthData(GenericViewSet):
    permission_classes=[AllowAny,]

    @action(methods=['POST'], detail=False)
    def departments(self, request):

        serializer = serializers.AddDepartmentSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()

            return Response({"details": "Added successfully"})

        return Response({"details": format_error(serializer.errors)})

    
    @action(methods=['POST'], detail=False)
    def roles(self, request):

        serializer = serializers.AddRemoveUserRolesSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()

            return Response({"details": "Roles Added successfully"})

        return Response({"details": format_error(serializer.errors)})

    




