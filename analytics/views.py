from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from app import settings
from authapp.serializers import CreateUserGeneralSerializer
from packages_service import models as p_models, serializers as p_serializers


# from .serializers import DepartmentDetailsSerializer, PublicUserBasicDetails, PublicUserDetailsSerializer, UserRolesSerializer
from authapp.models import DepartmentModel, UserModel
import jwt
from shared_utils.utils import get_user_by_id

from usermanagement.serializers import PublicUserBasicDetails

# Create your views here.


class GeneralView(GenericViewSet):
    
    def return_headers(self, request):
        headers = {
            "JWTAUTH":request.headers['JWTAUTH'].split(' ')[1],
            "Authorization":request.headers["Authorization"].split(' ')[1]
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
        return get_user_by_id(user_id)
    

class PackagesAnalytics(GeneralView):
    permission_classes=[]

    @action(methods=['GET'], detail=False)
    def get_counts(self, request):

        all_packages =  p_models.PackageModel.objects.all()
        all_packages_count = all_packages.count()
        active = all_packages.filter(is_active=True).count()
        in_active = all_packages.filter(is_active=False).count()
        # last_added_pack = all_packages.order_by('-date_created').first()

        # last_modified_pack =p_serializers.PackagesListStaffSerializer(
        #     all_packages.order_by('-date_modified').first(),
        #     many=False
        # ).data

        # persons_added_packages = set(all_packages.values('created_by'))

        # packs_per_person =[{
        #     'uploaded_by':PublicUserBasicDetails(
        #         get_user_by_id(user),
        #         many=False
        #         ).data,
        #     'packages': all_packages.filter(created_by=user).count(),
            
        #     } for user in persons_added_packages
        # ]

        res_object = {
            'all_packages_count':all_packages_count,
            # 'last_added_pack':last_added_pack,
            # 'last_modified_pack':last_modified_pack,
            # 'packs_per_person':packs_per_person,
            'active_packages':active,
            'inactive_packages':in_active
        }

        return Response(res_object)


class UsersAnalytics(GeneralView):

    @action(methods=['GET'], detail=False)
    def get_counts(self, request):
        
        all_users = UserModel.objects.all()
        verified = all_users.filter(is_email_verified=True).count()
        un_verified = all_users.filter(is_email_verified=False).count()
        active = all_users.filter(is_active=True).count()

        return_obj = {
            'all_users_count':all_users.count(),
            'verified_users': verified,
            'unverified_users': un_verified,
            'active_users': active
        }
        return Response(return_obj)

