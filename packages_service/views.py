from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
import jwt
from rest_framework.response import Response
from rest_framework import status, filters

from django.db.models import Q

from packages_service.models import PackageModel

from .serializers import PackagePublicViewSerializer, PackagesListStaffSerializer, PublicDetailViewSerializer
from .ingestion.utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import ListModelMixin

# Create your views here.
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


class PublicPackagesView(ListModelMixin, GeneralView):
    queryset = PackageModel.objects.filter(is_active__in=[True])
    serializer_class = PackagePublicViewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['description', 'title', 'requirements']
    filterset_fields = ['duration', 'tags', 'location']
    ordering_fields = ['date_created']
    ordering = ['-date_created']
    model = PackageModel
    permission_classes=(AllowAny,)

    def get_queryset(self):
        filter_ = self.request.query_params.get('filter')
        other_filters = self.request.query_params.get('other_filters')
        if filter_ not in ['', None]:
            return PackageModel.objects.filter(
                is_active__in=[True],
                tags__tag=filter_
                ) 
        if other_filters==True:
             return PackageModel.objects.filter(
                # is_active__in=[True],
                Q(tags__tag__in=[self.request.query_params.get('tags')], is_active__in=[True]) &
                Q(no_of_days__in=[self.request.query_params.get('duration')], is_active__in=[True]) |
                Q(city_town__in=[self.request.query_params.get('location')], is_active__in=[True])
                ).distinct()
        return super().get_queryset()


    @action(detail=False, methods=['GET'])
    def package_detail_view(self, request):
        
        try:
            pack = PackageModel.objects.get(id=request.query_params.get('package_id'))

        except PackageModel.DoesNotExist:
            return Response({"details": "Package not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicDetailViewSerializer(
            pack,
            many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StaffPackagesView(ModelViewSet):
    serializer_class = PackagesListStaffSerializer
    filterset_fields = ['city_town', 'country']
    search_fields = ['reference_number', 'description', 'requirements', 'tags__tag']
    ordering_fields = ['-date_created']
    ordering = ['-date_created']
    model = PackageModel
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        return PackageModel.objects.filter(is_active__in=[True, False])
    

    @action(detail=False, methods=['GET'])
    def package_detail_view(self, request):
        
        try:
            pack = PackageModel.objects.get(id=request.query_params.get('package_id'))

        except PackageModel.DoesNotExist:
            return Response({"details": "Package not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicDetailViewSerializer(
            pack,
            many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


