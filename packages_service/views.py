from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status

from packages_service.models import PackageModel

from .serializers import PackagePublicViewSerializer, PublicDetailViewSerializer
from .ingestion.utils import BookingPermission, SMTPermission
from shared_utils import utils

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.

class PackagesView(GenericViewSet, ListView):
    # permission_classes = [BookingPermission, SMTPermission ]
    serializer_class = PackagePublicViewSerializer
    paginate_by = 6
    model = PackageModel

    def get_queryset(self):
        return super().get_queryset()

    @action(detail=False, methods=['GET'])
    def packages_list(self, request):
       
       all_packs = PackageModel.objects.all().order_by("-date_created")
       paged = Paginator(all_packs, 6)
       
       pageered = paged.page(request.query_params.get('page'))

       serializer = PackagePublicViewSerializer(
        pageered,
        many=True
       )
       return Response({"data":serializer.data, "count":all_packs.count()})

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

