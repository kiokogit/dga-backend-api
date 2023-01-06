from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from packages_service.models import PackageModel

from .serializers import PackagePublicViewSerializer
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
       
       all_packs = PackageModel.objects.all().count()

    #    serializer = PackagePublicViewSerializer(
    #     all_packs
    #    )
       return Response(all_packs)