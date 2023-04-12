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
        user = UserModel.objects.filter(email=email, user_type=user_type).first()
        if user:
            return True, user
        else:
            return False, None

class SignUpUser(GenericViewSet):
    permission_classes = (AllowAny,)
    @staticmethod
    def get_user_by_email(email, user_type):
        user = UserModel.objects.filter(email=email, user_type=user_type).first()
        if user:
            return True, user
        else:
            return False, None


    @action(detail=False, methods=['POST'])
    def sign_up(self, request):
        # check is user exists
        if not request.data.get('email'):
            return Response({"details": "Email field cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        exists, instance = self.get_user_by_email(request.data.get('email'), request.data['user_type'])
        if exists:
            return Response({"details": "User with that email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        #serialized

        if request.data['user_type'] == 'PUBLIC USER':
            serializer = serializers.CreatePublicUserSerializer(
                data=request.data
            )
            
        elif request.data['user_type'] == 'INTERNAL STAFF':
            serializer = serializers.CreateInternalStaffUserSerializer(
                data=request.data,
                # context=self.return_serializer_context(request)
                context=None
            )
        
        else:
            serializer = serializers.CreateOrganizationUserSerializer(
                data=request.data
            )
            
        if serializer.is_valid():
            
            serializer.save()
            

            # user = UserModel.objects.get(email=request.data.get('email'))

            # token = Token.objects.create(user=user)

            # payload = {
            #     "user_id": str(user.id),
            #     "email": user.email,
            #     "user_type": user.user_type
            # }
            # jwt_token = jwt.encode(payload=payload, key=settings.SECRET_KEY)
            # # set headers
            # headers = {
            #     "JWTAUTH":f'Bearer {jwt_token}',
            #     "Authorization":f'Bearer {token}'
            # }
            
            return Response({"details":"User created successfully."}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            # TODO: Format serializer errors to user friendliness
            return Response({"details":format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def change_forgotten_password(self, request):
        # find user by email link sent
        pass
        

class LoginUser(ViewSet):
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        
        serializer = serializers.LoginUserSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"details": format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        # get user
        user_exists = False
        user = None
        try:
            user_exists, user = GeneralView.get_user_by_email(request.data.get('email'), request.data.get('user_type'))
        except Exception as e:
            print('There was a exception')
            print(e)
        if not user_exists:
            return Response({"details": "Invalid Email/Password"}, status=status.HTTP_400_BAD_REQUEST)
       
        # check is password match
        encoded = request.data.get('password').encode('utf-8')
        compare = bcrypt.checkpw(encoded, user.password.encode('utf-8'))
        if not compare:
            return Response({"details": "Invalid Email/Password"}, status=status.HTTP_400_BAD_REQUEST)
        # if exists, get payload for jwt token

        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)
        else:
            user.is_email_verified = True
            user.is_active = True
            user.save()

        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "user_type": user.user_type
        }
        jwt_token = jwt.encode(payload=payload, key=settings.SECRET_KEY)
        # set headers
        headers = {
            "JWTAUTH":f'Bearer {jwt_token}',
            "Authorization":f'Bearer {token}'
        }
        # pass in as headers
        return Response({"details": "User logged in successfully"}, headers=headers, status=status.HTTP_200_OK)
       

class UserRolesViewSet(GenericViewSet):

    permission_classes=(AllowAny)

    @action(methods=['GET'], detail=False)
    def get_department_roles(self, request):

        return

    @action(methods=['GET'], detail=False)
    def add_remove_user_role(self, request):

        serializer = None

        return
    