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


class PackagePublicViewSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=package_models.PackageModel
        fields=[
            'title',
            'cover_image',
            'package_particulars',
            'description',
            'id',
            'requirements',
            'cost'
        ]
    
    def get_cost(self, obj):

        return PackageCostSerializer(
            obj.price.all().ordered_by('amount').first(),
            many=False
        ).data


class LocationViewSerializer(serializers.ModelSerializer):

    class Meta:
        model=package_models.PackageLocationModel
        fields=[
            'country',
            'county',
            'city_town',
            'lat',
            'lng'
        ]

class TimelinesViewSerializer(serializers.ModelSerializer):

    class Meta:
        model=package_models.PackageTimelinesModel
        fields=[ 
            'package_from',
            'package_to',
            'no_of_days',
            'no_of_nights'
        ]

class PublicDetailViewSerializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(read_only=True)
    timelines=serializers.SerializerMethodField(read_only=True)
    location=serializers.SerializerMethodField(read_only=True)
    images=serializers.SerializerMethodField(read_only=True)
    related_events=serializers.SerializerMethodField(read_only=True)
    analytics=serializers.SerializerMethodField(read_only=True)
    cost=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=package_models.PackageModel
        fields=[
            'title',
            'cover_image',
            'package_particulars',
            'description',
            'id',
            'requirements',
            'cost',
            'reviews',
            'timelines',
            'images',
            'related_events',
            'analytics',
            'location',
        ]

    def get_location(self, obj):

        return LocationViewSerializer(
            obj.location.all(),
            many=True
        ).data

    def get_timelines(self, obj):

        return TimelinesViewSerializer(
            obj.duration,
            many=False
        ).data

    def get_images(self, obj):

        return [
                {"image": i['image'],
            "description": i['description']
            } for i in obj.images.all()
         ]

    def get_related_events(self, obj):

        return [
            {
                'event_name':e['event_name'],
                'event_from':e['event_from'],
                'event_to':e['event_to']
            } for e in obj.related_events.all()
        ]

    def get_cost(self, obj):

        return PackageCostSerializer(
            obj.price.all().ordered_by('amount'),
            many=True
        ).data

    def get_analytics(self, obj):

        return {}

    def get_reviews(self, obj):

        return {}
