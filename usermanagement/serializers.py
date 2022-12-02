from rest_framework import serializers
from authapp import models


class PublicUserBasicDetails(serializers.ModelSerializer):
    class Meta:
        model=models.PublicUserAccount
        fields=[
                "first_name",
                "email",
                "last_name",
                "middle_name",
            ]

class PublicUserDetailsSerializer(PublicUserBasicDetails):
    contact_details = serializers.SerializerMethodField(read_only=True)
    residential_address = serializers.SerializerMethodField(read_only=True)
    
    class Meta(PublicUserBasicDetails.Meta):
        fields= PublicUserBasicDetails.Meta.fields + [
            "id",
            "user_type",
            "date_created",
            "is_active",
            "is_deleted",
            "is_email_verified",
            "is_sms_verified",
            "contact_details",
            "residential_address"
        ]
    
    def get_contact_details(self, obj):
        details = models.ContactsModel.objects.filter(
            user__email=obj.email
        )
        if details.exists():
            return details[0].phone_number
        else:
            return "None"
        
    def get_residential_address(self, obj):
        address = models.ResidentialAddress.objects.filter(
            user__email=obj.email
        )
        if address.exists():
            return address[0]
        else:
            return "No Entry"

class UserRolesSerializer(serializers.Serializer):
    class Meta:
        model = models.RolesModel
        fields=[
            "role"
        ]