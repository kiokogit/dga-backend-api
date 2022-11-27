from urllib import response
from .models import PublicUserAccount, UserModel
from . import serializers
from app import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

import jwt
import bcrypt

class GeneralView(GenericViewSet):
    
    def return_headers(self, request):
        jwt_token = request.headers['JWTAUTH'].split(' ')[1]
        access_token = request.headers['Authorization'].split(' ')[1]
        return {
            'JWTAUTH':jwt_token,
            'Authorization':access_token
        }
    
    def get_serializer_context(self):
        context = {
            "headers": self.return_headers
        }
        return context
    
    @staticmethod
    def get_user_by_email(email, user_type):
        try:
            user = UserModel.objects.get(email=email, user_type=user_type)
            return True, user
        except UserModel.DoesNotExist:
            return False, None

class UsersAccountsManagerViewSet(GeneralView):
    
    @action(detail=False, methods=['POST'])
    def create_user(self, request):
        # check is user exists
        if not request.data.get('email'):
            return Response({"details": "Email field cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        #serialized
        if request.data['user_type'] == 'PUBLIC USER':
            serializer = serializers.CreatePublicUserSerializer(
                data=request.data
            )
            
        elif request.data['user_type'] == 'INTERNAL STAFF':
            serializer = serializers.CreateInternalStaffUserSerializer(
                data=request.data
            )
        
        else:
            serializer = serializers.CreateOrganizationUserSerializer(
                data=request.data
            )
            
        if serializer.is_valid():
            exists, user = self.get_user_by_email(request.data.get('email'), request.data['user_type'])
            if exists:
                return Response({"details": "User with that email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            
            return Response({"details":"User created successfully."}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            # TODO: Format serializer errors to user friendliness
            return Response({"details":"Invalid data. Cannot create user"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login_user(self, request):
        
        serializer = serializers.LoginUserSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"details": "Invalid User Data"}, status=status.HTTP_400_BAD_REQUEST)
        
        # get user
        user_exists, user = self.get_user_by_email(request.data.get('email'), request.data.get('user_type'))
        if not user_exists or user is None:
            return Response({"details": "Invalid Email/Password"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check is password match
        encoded = request.data.get('password').encode('utf-8')
        compare = bcrypt.checkpw(encoded, user.password.encode('utf-8'))
        if not compare:
            return Response({"details": "Invalid Email/Password"}, status=status.HTTP_400_BAD_REQUEST)
        # if exists, get payload for jwt token
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "user_type": user.user_type
        }
        jwt_token = jwt.encode(payload=payload, key=settings.SECRET_KEY).decode("utf-8")
        # set headers
        headers = {
            "JWTAUTH":f'Bearer {jwt_token}'
        }
        # pass in as headers
        return Response({"details": "User logged in successfully"}, headers=headers, status=status.HTTP_200_OK)
        

    @action(detail=False, methods=['POST'])
    def change_forgotten_password(self, request):
        # find user by email link sent
        pass
        
        
    