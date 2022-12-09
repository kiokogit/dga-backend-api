from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreatePackageBaseSerializer, CreatePackageValidateSerializer
from .utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.


class CreateTravelPackage(GenericViewSet):
    permission_classes = [BookingPermission, SMTPermission ]

    @action(detail=False, methods=['POST'])
    def create_new_package(self, request):
        
        serializer = CreatePackageValidateSerializer(
            data=request.data,
            context=utils.get_serializer_context(request)
        )
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({"details": "Package successfully added to database"}, status=status.HTTP_200_OK)

    

