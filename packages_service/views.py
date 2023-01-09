from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from packages_service.models import PackageModel

from .serializers import PackagePublicViewSerializer, PublicDetailViewSerializer
from .ingestion.utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.

class PackagesView(GenericViewSet):
    # permission_classes = [BookingPermission, SMTPermission ]
    serializer_class = PackagePublicViewSerializer

    def get_queryset(self):
        return super().get_queryset()

    @action(detail=False, methods=['GET'])
    def packages_list(self, request):
       
       all_packs = PackageModel.objects.all()

       serializer = PackagePublicViewSerializer(
        all_packs,
        many=True
       )
       return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def package_detail_view(self, request):
        
        try:
            pack = PackageModel.objects.get(package_id=request.query_params.get('package_id'))

        except PackageModel.DoesNotExist:
            return Response({"details": "Package not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicDetailViewSerializer(
            pack,
            many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

