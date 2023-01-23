import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreatePackageBaseSerializer, CreatePackageValidateSerializer
from .utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .. import models as package_models


# Create your views here.


class CreateTravelPackage(GenericViewSet):
    # permission_classes = [BookingPermission, SMTPermission ]

    @action(detail=False, methods=['POST'])
    def create_new_package(self, request):
        
        serializer = CreatePackageValidateSerializer(
            data=request.data,
            context=utils.get_serializer_context(request)
        )
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({"details": "Package successfully added to database"}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['POST'])
    def delete_package(self, request):
        try:
            pack = package_models.PackageModel.objects.get(package_id=request.query_params.get('id'))

        except package_models.PackageModel.DoesNotExist or TypeError:
            return Response({"details":"Package does not exist. Wrong ID passed"}, status=status.HTTP_400_BAD_REQUEST)

        pack.is_active = False
        pack.is_deleted = True
        pack.date_deleted = datetime.datetime.now()
        pack.save()
        
        return Response({"details":"Package successfully removed from database"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def activate_deactivate_package(self, request):
        try:
            pack = package_models.PackageModel.objects.get(package_id=request.query_params.get('package_id'))

        except package_models.PackageModel.DoesNotExist or TypeError:
            return Response({"details":"Package does not exist. Wrong ID passed"}, status=status.HTTP_400_BAD_REQUEST)

        if pack.is_active:
            pack.is_active = False
        else:
            pack.is_active = True
        pack.is_deleted = False
        pack.date_deleted = None
        pack.save()

        return Response({"details":"Package successfully Updated"}, status=status.HTTP_200_OK)


