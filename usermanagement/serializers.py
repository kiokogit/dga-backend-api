from rest_framework import serializers
from authapp import models


class PublicUserBasicDetails(serializers.ModelSerializer):
    class Meta:
        model=models.UserModel
        fields=[
                "first_name",
                "email",
                "last_name",
                "middle_name",
            ]

class PublicUserDetailsSerializer(PublicUserBasicDetails):
    # contact_details = serializers.SerializerMethodField(read_only=True)
    # residential_address = serializers.SerializerMethodField(read_only=True)
    # roles = serializers.SerializerMethodField(read_only=True)
    
    class Meta(PublicUserBasicDetails.Meta):
        fields= PublicUserBasicDetails.Meta.fields + [
            "id",
            "user_type",
            "date_created",
            "is_active",
            "is_deleted",
            "is_email_verified",
            "is_sms_verified",
            # "contact_details",
            # "residential_address",
            # "roles",
            "department_id",
            "profile_pic"
        ]
    
    # def get_contact_details(self, obj):
    #     details = models.ContactsModel.objects.filter(
    #         user__email=obj.email
    #     )
    #     if details.exists():
    #         return details[0].phone_number
    #     else:
    #         return "None"
        
    # def get_residential_address(self, obj):
        
    #     return "No Entry"

    # def get_roles(self, obj):
    #     roles = obj.roles.filter(is_active=True)
    #     return UserRolesSerializer(
    #         roles,
    #         many=True
    #     ).data


class UserRolesSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    department_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.RolesModel
        fields=[
            "role",
            "is_department_head",
            'id',
            'department',
            'department_id'
        ]

    def get_department(self, obj):
        return obj.department.name
    
    def get_department_id(self, obj):
        return obj.department.id
    
class DepartmentDetailsSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.DepartmentModel
        fields=[
            'name',
            'id',
            'roles'
        ]

    def get_roles(self, obj):

        return UserRolesSerializer(
            obj.department_roles,
            many=True
        ).data