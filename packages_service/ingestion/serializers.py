import datetime
from rest_framework import serializers
from django.db import transaction

from shared_utils.utils import generate_package_ref
from .. import models as package_models


class PriceValidateSerializer(serializers.Serializer):
    type=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    currency=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    amount=serializers.CharField(required=False, allow_blank=True, allow_null=True)

class TimelinesSerializer(serializers.Serializer):
    package_from=serializers.DateTimeField(required=False, allow_null=True)
    package_to=serializers.DateTimeField(required=False, allow_null=True)
    no_of_days=serializers.IntegerField(required=False, allow_null=True)
    no_of_nights=serializers.IntegerField(required=False, allow_null=True)

    def validate_package_from(self, attrs):
        if attrs['package_from'] < datetime.datetime.now():
            raise serializers.ValidationError("Kindly choose a date or time later than now/today for start date")
        if attrs['package_from'] >= attrs["package_to"]:
            raise serializers.ValidationError("Please choose start date lower than the end date.")
        return attrs
        

class LocationSerializer(serializers.Serializer):
    country=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    county=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    city_town=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    lat = serializers.CharField(required=False, max_length=50, allow_blank=True, allow_null=True)
    lng = serializers.CharField(required=False, max_length=50, allow_blank=True, allow_null=True)

class TieToEventSerializer(serializers.Serializer):
    event_name=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    event_from=serializers.DateTimeField(required=False, allow_null=True)
    event_to=serializers.DateTimeField(required=False, allow_null=True)

class PackageDetailsSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    package_particulars = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    requirements = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cover_image = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    tie_to_event = serializers.BooleanField(allow_null=True)
    expire_after_event = serializers.BooleanField(allow_null=True)

class CreatePackageBaseSerializer(serializers.Serializer):
    package = PackageDetailsSerializer()
    images = serializers.ListField(
        required=False,
        child=serializers.CharField(required=True, allow_null=True, allow_blank=True),
        allow_null=True
        )

    location_details = LocationSerializer()
    price = serializers.ListField(
        required=False,
        child=PriceValidateSerializer(),
        allow_null=True
        )

    timelines = TimelinesSerializer()
    event = TieToEventSerializer()

class CreatePackageValidateSerializer(CreatePackageBaseSerializer):

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.package = None

    def validate(self, attrs):
        # 
        return attrs

    def create(self, validated_data):
        reference_number = generate_package_ref()

        with transaction.atomic():     
            # create package
            self.package = package_models.PackageModel.objects.create(
                **validated_data['package'],
                reference_number=reference_number,
                created_by=self.context['user']
            )

            # location
            package_models.PackageLocationModel.objects.create(
                **validated_data['location_details'],
                package=self.package
            )

            # prices
            [
                package_models.PackageCurrencyModel.objects.create(
                    **i,
                    package=self.package
                ) for i in validated_data['price']
            ]

            # images
            [
                package_models.PackageImagesModel.objects.create(
                    image=i,
                    uploaded_by=self.context['user'],
                    package=self.package
                ) for i in validated_data['images']
            ]

            # timelines
            package_models.PackageTimelinesModel.objects.create(
                **validated_data['timelines'],
                package=self.package
            )

            # tie to event
            if validated_data['tie_to_event']:
                package_models.PackageRelatedEvent.objects.create(
                    **validated_data['event'],
                    package=self.package
                )

        return validated_data

