from rest_framework import serializers

from .utils import CreateUserRoles
from .models import ContactsModel, PublicUserAccount, StaffUserAccount, RolesModel
import bcrypt

class CreateUserGeneralSerializer(serializers.Serializer):
    password=serializers.CharField(required=True)
    password2=serializers.CharField(required=True)
    first_name=serializers.CharField(required=False)
    last_name=serializers.CharField(required=False)
    middle_name=serializers.CharField(required=False)
    email=serializers.EmailField(required=True)
    
    
    def validate(self, data):
        # check passwords
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match')
        del data['password2']
        
        # hash password
        salt = bcrypt.gensalt()
        try:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
            data['password'] = hashed_password.decode('utf-8')
        except Exception as e:
            raise serializers.ValidationError('Error hashing password')
        
        return data
    

class CreatePublicUserSerializer(CreateUserGeneralSerializer):
    # attempts to create a user account in the following circumstances:
    # 1. if public user is booking for a journey, a default account is create using the entered details is created. Password is filled at the end, username filled, confirmed email may also be used
    # 2. deliberate "register" function by a public user
    # 3. if writing a review. if not logged in, on submitting the email, create account, and ask for password and username(optional)
    # 4. If trying to add to cart, prompt to register a base account
    """for general public user"""
    
    def validate(self, data):
        
        return super().validate(data)
        
    def create(self, validated_data):
        
        try:
            PublicUserAccount.objects.create(
                **validated_data
            )
        except Exception:
            raise serializers.ValidationError("There was an error creating user")
        
        # Todo: send confirmation to email/phone if entered
        
        return validated_data
    
class CreateInternalStaffUserSerializer(CreateUserGeneralSerializer):
    """for general internal staff, eg director, customer care"""

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.error_messages = []

    roles=serializers.ListField(
        required=True,
        child=serializers.CharField(required=True, allow_blank=False, allow_null=False)
    )

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):

        try:
            staff_user = StaffUserAccount.objects.create(
                **validated_data
            )

        except Exception:
            raise serializers.ValidationError("There was an error creating staff user")

        for role in self.roles:  # type: ignore
            created, message = CreateUserRoles (
            user=staff_user, 
            role=role,
            actor=self.context["user_id"]
            ).add_user_role()

            if not created:
                raise serializers.ValidationError(message)
        
        return validated_data

class CreateSystemAccountsSerializer(CreateUserGeneralSerializer):
    """for system admins, superusers"""
    pass


class CreateOrganizationUserSerializer(CreateUserGeneralSerializer):
    """for organizations"""
    name=serializers.CharField(required=True),
    industry=serializers.CharField(required=True)
    

class LoginUserSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True)
    user_type=serializers.CharField(required=True)
    
    def validate(self, attrs):
        
        return attrs
    