from rest_framework import serializers

from shared_utils.models import NotificationsModel


class NotificationsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotificationsModel
        fields = '__all__'



