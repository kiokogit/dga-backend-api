from datetime import timezone
from django.db import models
import uuid
from .constants import USER_TYPES, ROLES
# Create your models here.

# basic model
class BaseModel(models.Model):
    id=models.UUIDField(default=uuid.uuid4(), primary_key=True, max_length=50, editable=False)
    date_created=models.DateTimeField(auto_now=True) 
    date_modified=models.DateTimeField(auto_now_add=True)
    
    
class BaseModelWithStatus(BaseModel):
    is_active=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    date_deleted=models.DateTimeField(blank=True, null=True)


# basic user model
class BaseUserModel(BaseModelWithStatus):
    is_email_verified=models.BooleanField(default=False)
    is_sms_verified=models.BooleanField(default=False)
    email=models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=255)
    

# basic user
class UserModel(BaseUserModel):
    first_name=models.CharField(max_length=50, null=True, blank=True)
    middle_name=models.CharField(max_length=50, null=True, blank=True)
    last_name=models.CharField(max_length=50, null=True, blank=True)
    user_type=models.CharField(max_length=25, default="PUBLIC USER", choices=USER_TYPES)
    
    
# public user
class PublicUserAccount(UserModel):
    
    def __str__(self) -> str:
        return self.email   
    

# staff user
class StaffUserAccount(UserModel):
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_general_staff=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email
    
# Organization account
class OrganizationAccount(BaseUserModel):
    name=models.CharField(max_length=255)
    industry=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email + ' ' + self.name

# otp model
class OTPVerification(BaseModelWithStatus):
    user=models.ForeignKey(UserModel, related_name="otp_verification", on_delete=models.CASCADE) 
    verified=models.CharField(max_length=255, null=True, blank=True)
    otp_code=models.CharField(max_length=255, null=True, blank=True)
    mode=models.CharField(max_length=255, null=True, blank=True)
    
    
# residential address for public
class ResidentialAddress(BaseModelWithStatus):
    user=models.ForeignKey(PublicUserAccount, related_name='user_location', on_delete=models.CASCADE) 
    country=models.CharField(max_length=50, null=True, blank=True)
    state=models.CharField(max_length=50, null=True, blank=True)
    county=models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    town=models.CharField(max_length=50, null=True, blank=True)
    estate=models.CharField(max_length=50, null=True, blank=True)
    plot_number=models.CharField(max_length=50, null=True, blank=True)
    house_number=models.CharField(max_length=50, null=True, blank=True)
    geo_location=models.TextField(blank=True, null=True)
    

# user roles
class RolesModel(BaseModelWithStatus):
    user=models.ForeignKey(UserModel, related_name="roles", on_delete=models.CASCADE)
    role=models.CharField(max_length=25, choices=ROLES, default="GENERAL STAFF")

# user contacts
class ContactsModel(models.Model):
    user=models.ForeignKey(UserModel, related_name="contact_details", on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=50, null=True, blank=True)
    is_phone_number_verified=models.BooleanField(default=False)
    alternative_phone_number=models.CharField(max_length=50, null=True, blank=True)
    is_alternative_phone_number_verified=models.BooleanField(default=False)

class ProfessionalAccountsModel(BaseModelWithStatus):
    account_name = models.CharField(max_length=50, unique=True)
    account_roles = models.ForeignKey(RolesModel, related_name='roles', on_delete=models.CASCADE)

class ProfessionalUpgradesModel(BaseModelWithStatus):
    user = models.ForeignKey(UserModel, related_name="professional_upgrade", on_delete=models.CASCADE)
    professional_account = models.ForeignKey(ProfessionalAccountsModel, related_name='professional_accounts', on_delete=models.CASCADE)
    upgraded_by = models.CharField(max_length=50, null=True, blank=True)


