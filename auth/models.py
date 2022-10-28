from datetime import timezone
from django.db import models
import uuid
import bcrypt
# Create your models here.

# basic model
class BaseModel(models.Model):
    id=models.UUIDField(default=uuid.uuid4(), primary_key=True, max_length=50)
    date_created=models.DateTimeField(auto_add=True)
    date_modified=models.DateTimeField(auto_add_now=True)
    is_deleted=models.BooleanField(default=False)

# basic user model
class BaseUserModel(BaseModel):
    is_active=models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    is_sms_verified=models.BooleanField(default=False)

# basic user
class UserModel(BaseUserModel):
    first_name=models.CharField(max_length=50, null=True, blank=True)
    middle_name=models.CharField(max_length=50, null=True, blank=True)
    last_name=models.CharField(max_length=50, null=True, blank=True)
    phone_number=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(max_length=255, null=True, blank=True)
    password=models.CharField(max_length=255, null=True, blank=True)
    
    def encrypt_password(self, password):
        # validate length
        salt = bcrypt.genSalt()
        return bcrypt.hashpw(password, salt)
    
# public user
class PublicUserAccount(UserModel):
    username=models.CharField(max_length=50, null=True, blank=True)