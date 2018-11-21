from rest_framework import serializers
from . import models
from dunqgram.users import models as user_models
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = ('__all__')
