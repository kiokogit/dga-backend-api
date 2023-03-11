import datetime
from rest_framework import serializers
from django.db import transaction

from shared_utils.utils import generate_package_ref
from .. import models as package_models


class PriceValidateSerializer(serializers.Serializer):
    type=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    currency=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    amount=serializers.CharField(required=False, allow_blank=True, allow_null=True)
 

class PackageDetailsSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    package_particulars = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    requirements = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    cover_image = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    tie_to_event = serializers.BooleanField(allow_null=True)
    expire_after_event = serializers.BooleanField(allow_null=True)
    event_name=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    event_from=serializers.DateTimeField(required=False, allow_null=True)
    event_to=serializers.DateTimeField(required=False, allow_null=True)
    country=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    county=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    city_town=serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    lat = serializers.CharField(required=False, max_length=50, allow_blank=True, allow_null=True)
    lng = serializers.CharField(required=False, max_length=50, allow_blank=True, allow_null=True)
    package_from=serializers.DateTimeField(required=False, allow_null=True)
    package_to=serializers.DateTimeField(required=False, allow_null=True)
    no_of_days=serializers.IntegerField(required=False, allow_null=True)
    no_of_nights=serializers.IntegerField(required=False, allow_null=True)

class CreatePackageBaseSerializer(serializers.Serializer):
    package = PackageDetailsSerializer()
    images = serializers.ListField(
        required=False,
        child=serializers.DictField(required=True),
        allow_null=True
        )

    price = serializers.ListField(
        required=False,
        child=PriceValidateSerializer(),
        allow_null=True
        )
    tags = serializers.ListField(
        required=False,
        child=serializers.CharField(required=True, max_length=50),
        allow_null=True
        )

class CreatePackageValidateSerializer(CreatePackageBaseSerializer):

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.package = None

    def validate(self, attrs):
        # if not staff
        # if self.context['user_type'] != "STAFF":
        #     raise serializers.ValidationError("You do not have permission to perform this action.")
        return attrs

    def create(self, validated_data):
        reference_number = generate_package_ref()

        with transaction.atomic():     
            # create package
            self.package = package_models.PackageModel.objects.create(
                **validated_data['package'],
                reference_number=reference_number,
                created_by=self.context['user_id']
            )

            new_tags = []
            for t in validated_data['tags']:
                tag_exists = package_models.TagsModel.objects.all().filter(tag=t.lower())
                if not tag_exists.exists():
                    tag = package_models.TagsModel.objects.create(
                    tag=t.lower()
                        )
                    new_tags.append(tag)
                else:
                    new_tags.append(tag_exists.first())
        
            self.package.tags.set(new_tags)
            self.package.save()

            # images
            [
                package_models.PackageImagesModel.objects.create(
                    image=i['image'],
                    description=i['description'],
                    package_id=self.package.id
                ) for i in validated_data['images']
            ]

            # prices/costs list
            [
                package_models.PackageCurrencyModel.objects.create(
                    type=i['type'],
                    amount=i['amount'],
                    currency=i['currency'],
                    package_id=self.package.id
                ) for i in validated_data['price']
            ]

        return validated_data


class DeleteArchiveRestorePackageSerializer(serializers.Serializer):
    request_id = serializers.CharField(required=True)
    delete_archive_restore = serializers.CharField(required=True)
    


class EditPackageSerializer(serializers.Serializer):


    def validate(self, attrs):
        try:
            package_instance = package_models.PackageModel.objects.filter(id=attrs['package']['package_id'])

        except package_models.PackageModel.DoesNotExist or TypeError:
            raise serializers.ValidationError("Package does not exist. Wrong ID passed")

        return attrs

    def create(self, validated_data):
        print(validated_data)
        try:
            package_instance = package_models.PackageModel.objects.filter(id=validated_data['package']['package_id'])

        except package_models.PackageModel.DoesNotExist or TypeError:
            raise serializers.ValidationError("Package does not exist. Wrong ID passed")

        # save package data
        try:
            package_instance.update(**validated_data['package']) # type:ignore
        except Exception as e:
            print(e)
        images = validated_data['images']
        current_images = package_models.PackageImagesModel.objects.filter(
            id=package_instance.first().package_id  # type:ignore
        ).all()
        for i in current_images:
            if i not in images:
                i.is_active=False
                i.save()
        for i in images:
            if i not in current_images:
                package_models.PackageImagesModel.objects.create(
                    id=package_instance.first().package_id  # type:ignore
                    **i
                )
            

        return validated_data

