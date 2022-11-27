from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.


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


class CreateTravelPackage(GeneralView):

    @action(detail=False, methods=['POST'])
    def create_new_package(self, request):
        
        pass


