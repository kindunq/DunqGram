from rest_framework import serializers
from . import models
from dunqgram.images import serializers as images_serialzers


class UserProfileSerializer(serializers.ModelSerializer):
    images = images_serialzers.CountImageSerializer(many=True, read_only=True)
    # readonly no modify
    post_count = serializers.ReadOnlyField() 
    followers_count = serializers.ReadOnlyField() 
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images'
        )


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
        )
