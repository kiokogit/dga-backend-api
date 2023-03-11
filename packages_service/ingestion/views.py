import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreatePackageBaseSerializer, CreatePackageValidateSerializer, EditPackageSerializer
from .utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from .. import models as package_models

import re


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
            pack = package_models.PackageModel.objects.get(id=request.query_params.get('id'))

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
            pack = package_models.PackageModel.objects.get(id=request.query_params.get('package_id'))

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

    @action(detail=False, methods=['POST'])
    def edit_package_details(self, request):
        validated_data = request.data

    # save package data
        try:
            package_instance = package_models.PackageModel.objects.filter(package_id=validated_data['package']['package_id'])

        except package_models.PackageModel.DoesNotExist or TypeError:
            return ("Package does not exist. Wrong ID passed")

        # save package data
        try:
            package_instance.update(**validated_data['package']) # type:ignore
        except Exception as e:
            print(e)
        images = validated_data['images']
        current_images = package_models.PackageImagesModel.objects.filter(
            package_id=package_instance.first().id  # type:ignore
        ).all()
        for i in current_images:
            if i not in images:
                i.is_active=False
                i.save()
        for i in images:
            if i not in current_images:
                package_models.PackageImagesModel.objects.create(
                    package_id=package_instance.first().id  # type:ignore
                    **i
                )
            

        return Response({"details":"details not updated."}, status=status.HTTP_400_BAD_REQUEST)

