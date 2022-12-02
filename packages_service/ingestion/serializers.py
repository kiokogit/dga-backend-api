import datetime
from rest_framework import serializers

from shared_utils.utils import generate_package_ref


class PriceValidateSerializer(serializers.Serializer):
    type=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    currency=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    amount=serializers.CharField(required=False, allow_blank=True, allow_null=True)

class TimelinesSerializer(serializers.Serializer):
    package_from=serializers.DateTimeField(required=False, blank=True, null=True)
    package_to=serializers.DateTimeField(required=False, blank=True, null=True)
    no_of_days=serializers.IntegerField(required=False, blank=True, null=True)
    no_of_nights=serializers.IntegerField(required=False, blank=True, null=True)

    def validate_package_from(self, attrs):
        if attrs['package_from'] < datetime.datetime.now():
            raise serializers.ValidationError("Kindly choose a date or time later than now/today for start date")
        if attrs['package_from'] >= attrs["package_to"]:
            raise serializers.ValidationError("Please choose start date lower than the end date.")
        return attrs
        

class LocationSerializer(serializers.Serializer):
    country=serializers.CharField(required=False, max_length=100, blank=True, null=True)
    county=serializers.CharField(required=False, max_length=100, blank=True, null=True)
    city_town=serializers.CharField(required=False, max_length=100, blank=True, null=True)
    lat = serializers.CharField(required=False, max_length=50, blank=True, null=True)
    lng = serializers.CharField(required=False, max_length=50, blank=True, null=True)

class CreatePackageBaseSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    package_particulars = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    requirements = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cover_image = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    images = serializers.ListField(
        required=False,
        child=serializers.CharField(required=True, allow_null=True, allow_blank=True),
        allow_null=True,
        allow_blank=True
        )

    location_details = LocationSerializer()
    price = PriceValidateSerializer()
    timelines = TimelinesSerializer()


class CreatePackageValidateSerializer(CreatePackageBaseSerializer):

    def validate(self, attrs):
        # 
        return attrs

    def create(self, validated_data):
        reference_number = generate_package_ref()
        
