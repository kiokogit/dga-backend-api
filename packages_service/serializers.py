import datetime
from rest_framework import serializers
from django.db import transaction

from . import models as package_models


class PackageCostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=package_models.PackageCurrencyModel
        fields=[
            'amount',
            'type',
            'currency'
        ]

class PackageImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model=package_models.PackageImagesModel
        fields=[
            'image',
            'description'
        ]


class PackagePublicViewSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=package_models.PackageModel
        fields=[
            'title',
            'cover_image',
            'package_particulars',
            'description',
            'package_id',
            'requirements',
            'cost',
            'reference_number'
        ]
    
    def get_cost(self, obj):

        return PackageCostSerializer(
            package_models.PackageCurrencyModel.objects.filter(
                package_id=obj.package_id
            ).order_by('-amount').first(),
            many=False
        ).data

class PublicDetailViewSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    images=serializers.SerializerMethodField(read_only=True)
    cost=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=package_models.PackageModel
        fields=[
            'reference_number',
            'title',
            'cover_image',
            'package_particulars',
            'description',
            'package_id',
            'requirements',
            'cost',
            'reviews',
            'package_from',
            'package_to',
            'no_of_days',
            'no_of_nights',
            'event_from',
            'event_to',
            'event_name',
            'images',
            'country',
            'county',
            'city_town',
            'lat',
            'lng',
            'likes',
            'dislikes'
        ]

    def get_images(self, obj):

        return PackageImagesSerializer(
            package_models.PackageImagesModel.objects.filter(
                package_id=obj.package_id
            ).all(),
            many=True
        ).data


    def get_reviews(self, obj):

        return {}

    def get_cost(self, obj):

        return PackageCostSerializer(
            package_models.PackageCurrencyModel.objects.filter(
                package_id=obj.package_id
            ).all(),
            many=True
        ).data
