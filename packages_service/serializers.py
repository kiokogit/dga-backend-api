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
            'description',
            'id',
            'cost',
            'reference_number',
            'no_of_days',
            'no_of_nights',
        ]
    
    def get_cost(self, obj):

        return PackageCostSerializer(
            package_models.PackageCurrencyModel.objects.filter(
                package_id=obj.id
            ).first(),
            many=False
        ).data


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model=package_models.TagsModel
        fields=['tag']

class PublicDetailViewSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    images=serializers.SerializerMethodField(read_only=True)
    cost=serializers.SerializerMethodField(read_only=True)
    categories=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=package_models.PackageModel
        fields=[
            'reference_number',
            'title',
            'cover_image',
            'package_particulars',
            'description',
            'id',
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
            'dislikes', 
            'categories',
            "is_active",
        ]

    def get_images(self, obj):

        return PackageImagesSerializer(
            package_models.PackageImagesModel.objects.filter(
                package_id=obj.id
            ).all(),
            many=True
        ).data


    def get_reviews(self, obj):

        return {}

    def get_cost(self, obj):

        return PackageCostSerializer(
            package_models.PackageCurrencyModel.objects.filter(
                package_id=obj.id
            ).all(),
            many=True
        ).data

    def get_categories(self, obj):
        return TagsSerializer(
            obj.tags.all().values('tag'),
            many=True
        ).data



class PackagesListStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model=package_models.PackageModel
        fields=[
            'title',
            'cover_image',
            'description',
            'id',
            'reference_number',
            "is_active",
            'city_town',
            'country'
        ]
