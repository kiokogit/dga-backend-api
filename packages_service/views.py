from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

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

    @action(detail=False, methods=['GET'])
    def package_by_tags(self, request):

        filters = request.query_params.get("filter").split(',')
        if filters[0]!="":
            all_packs = PackageModel.objects.filter(
                tags__tag__in=filters
            ).all().order_by("-date_created")
        else:
            all_packs = PackageModel.objects.all().order_by("-date_created")
    
        paged = Paginator(all_packs, 6)
       
        pageered = paged.page(request.query_params.get('page'))

        serializer = PackagePublicViewSerializer(
            pageered,
            many=True
        )

        query_set = {
            "data":serializer.data, 
            "count":all_packs.count(),
            "tags":filters
            }
        return Response(query_set, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def packages_search(self, request):
        search_value = request.query_params.get('SEARCH')
        all_packs = PackageModel.objects.filter(
            Q(title__contains=search_value) | 
            Q(tags__tag__in=search_value) |
            Q(description__contains=search_value) |
            Q(country__contains=search_value) |
            Q(county__contains=search_value) |
            Q(city_town__contains=search_value)
        ).all().order_by('-date_created').distinct()

        paged = Paginator(all_packs, 6)
       
        pageered = paged.page(request.query_params.get('page'))

        serializer = PackagePublicViewSerializer(
            pageered,
            many=True
        )

        query_set = {
            "data":serializer.data, 
            "count":all_packs.count(),
            "tags":[search_value]
            }
        return Response(query_set, status=status.HTTP_200_OK)