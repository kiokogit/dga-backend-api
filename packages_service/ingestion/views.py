from django.shortcuts import render
from .utils import BookingPermission, SMTPermission

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.


class CreateTravelPackage(GenericViewSet):
    permission_classes = [BookingPermission, SMTPermission ]

    @action(detail=False, methods=['POST'])
    def create_new_package(self, request):
        
        pass


