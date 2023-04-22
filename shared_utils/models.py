from django.db import models

from authapp.models import BaseModelWithStatus, UserModel

# Create your models here.

class InfoBaseModel(BaseModelWithStatus):
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)

    ordered_by = ['-date_modified']


class MessagesModel(InfoBaseModel):
    attachment = models.TextField(blank=True, null=True)
    

class NotificationsModel(InfoBaseModel):
    urgent = models.BooleanField(default=False)

    

