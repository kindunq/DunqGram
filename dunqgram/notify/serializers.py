from rest_framework import serializers
from . import models
from dunqgram.users import serializers as user_serializer
from dunqgram.images import serializers as image_serializer


class NotifySerializers(serializers.ModelSerializer):
    creator = user_serializer.ListUserSerializer()
    image = image_serializer.SmallImageSerializer()

    class Meta:
        model = models.Notify
        fields = ('__all__')
