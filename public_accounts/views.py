from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from app import settings
from authapp.serializers import CreateUserGeneralSerializer

from .serializers import PublicUserBasicDetails, PublicUserDetailsSerializer
from authapp.models import UserModel
import jwt

# Create your views here.


class GeneralView(GenericViewSet):
    
    def return_headers(self, request):
        headers = {
            "JWTAUTH":request.headers['JWTAUTH'].split(' ')[1],
            # "Authorization":request.headers["Authorization"].split(' ')[1]
        }
        return headers
    
    def get_serializer_context(self, request):
        headers = self.return_headers(request)
        # decode jwt
        payload = jwt.decode(headers['JWTAUTH'],key=settings.SECRET_KEY, algorithms=['HS256'])
        
        context = {
            "user_id": payload['user_id'],
            "user_type": payload['user_type'],
            "headers":headers
        }
        return context
    
    def get_logged_in_user(self, request):
        user_id = self.get_serializer_context(request)['user_id']
        # get user by ID
        return self.get_user_by_id(user_id)
    
    def get_user_by_id(self, id):
        try:
            user = UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return None
        return user

class PublicAccountsViewSet(GeneralView):
    
    @action(detail=False, methods=['GET'])
    def get_user_own_profile(self, request):
        
        user = self.get_logged_in_user(request)
        
        if user is None:
            return Response({"details": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PublicUserDetailsSerializer(
            user,
            many=False
        )
        
        return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        
    
    @action(detail=False, methods=['GET'])
    def get_user_public_profile(self, request):
        if not request.query_params.get('user_id'):
            return Response({"details": "User id is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_user_by_id(request.query_params.get('user_id'))
        if user is None:
            return Response({"details": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PublicUserBasicDetails(
            user,
            many=False
        )
        
        return Response({"details": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def change_user_password(self, request):
        # must be logged in user
        user = self.get_logged_in_user(request)
        
        if user is None:
            return Response({"details": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # new password hash
        serializer = CreateUserGeneralSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"details": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.password = serializer.data['password']
        user.save(update_fields=['password'])
        return Response({"details": "Password Changed Successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def update_user_profile(self, request):
        
        pass