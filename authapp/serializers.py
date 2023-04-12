from django.conf import settings
from rest_framework import serializers
from django.db import transaction
from .utils import CreateUserRoles, add_user_role, generate_random_password, send_staff_account_signup, sendemail, validate_email, validate_password
from .models import ContactsModel, DepartmentModel, RolesModel, UserModel
import bcrypt


class CreateUserGeneralSerializer(serializers.Serializer):
    password=serializers.CharField(required=False)
    # password2=serializers.CharField(required=True)
    first_name=serializers.CharField(required=False)
    last_name=serializers.CharField(required=False)
    middle_name=serializers.CharField(required=False)
    email=serializers.EmailField(required=True)
    user_type=serializers.CharField(required=True)
    
    
    def validate(self, data):

        data['password'] = generate_random_password()

        if not validate_email(data['email']):
            raise serializers.ValidationError('Email does not meet basic requirements for an email.')
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
            UserModel.objects.create(
                **validated_data
            )
        except Exception:
            raise serializers.ValidationError("There was an error creating user")
        
        # Todo: send confirmation to email/phone if entered
        
        return validated_data

class StaffCreateUserSerializer(serializers.Serializer):
    is_general_staff = serializers.BooleanField(default=True) # type: ignore
    is_superuser = serializers.BooleanField(default=False) # type: ignore
    is_admin = serializers.BooleanField(default=False) # type: ignore
    roles = serializers.ListField(
        required=True,
        child = serializers.CharField(required=True)
    )

    
class CreateInternalStaffUserSerializer(CreateUserGeneralSerializer, StaffCreateUserSerializer):
    """for general internal staff, eg director, customer care"""

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.error_messages = []

    
    def validate(self, data):
        # check user has permission to add specified roles
        for role_id in data['roles']:  # type: ignore
            role_instance = RolesModel.objects.get(id=role_id)
            has_perm = CreateUserRoles(
                user=None,
                role=role_instance,
                actor=self.context['user_id'],
                department_id=role_instance.department.id # type: ignore
            ).actor_has_permission()
            if not has_perm:
                raise serializers.ValidationError(f"You do not have permission to add a user with the role of a {role_instance.role}.")

        return super().validate(data)

    def create(self, validated_data):
        # ... code to create user ...
        if "CHIEF ICT OFFICER" in validated_data['roles']:
            validated_data['is_superuser'] = True
            validated_data['is_admin'] = True

        # # try:
        with transaction.atomic():
             
            # hash password
            salt = bcrypt.gensalt()

            user = UserModel.objects.create(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                middle_name=validated_data["middle_name"],
                password=(bcrypt.hashpw(validated_data['password'].encode('utf-8'), salt)).decode('utf-8'),
                email=validated_data["email"],
                user_type=validated_data['user_type'],
                is_admin=validated_data["is_admin"],
                is_superuser=validated_data["is_superuser"],
                is_general_staff=validated_data["is_general_staff"]
            )

            user = UserModel.objects.get(email=validated_data['email'])

            for role_id in validated_data['roles']:  # type: ignore
                role_instance = RolesModel.objects.get(id=role_id)
                created, message = CreateUserRoles(
                    user=user,
                    role=role_instance,
                    actor=self.context['user_id'],
                    department_id=role_instance.department.id #type:ignore
                ).add_user_role()

                if not created:
                    raise serializers.ValidationError(message)
        send_staff_account_signup(to_email=validated_data['email'], password=validated_data['password'])
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
    

class AddDepartmentSerializer(serializers.Serializer):
    names = serializers.ListField(
        child=serializers.CharField()
    )


    def create(self, validated_data):

        [ DepartmentModel.objects.create(
            name=name
        ) for name in validated_data['names']]

        return validated_data



class AddRemoveUserRolesSerializer(serializers.Serializer):
    # user_id = serializers.UUIDField()
    # role_id = serializers.UUIDField()
    # add_remove = serializers.CharField()
    roles = serializers.ListField(
        child=serializers.DictField()
    )


    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        with transaction.atomic():
            departments = DepartmentModel.objects.all()
            for department in departments:
                [RolesModel.objects.create(
                    role=i['role'],
                    department=department,
                    is_primary_role=i['is_primary_role'],
                    is_department_head=i['is_department_head']
                ) for i in validated_data['roles'] if (department.name==i['department'] and not RolesModel.objects.filter(role=i['role']).exists())
                ]

        return super().create(validated_data)
