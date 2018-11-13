from rest_framework import serializers
from . import models
from dunqgram.images import serializers as images_serialzers


class UserProfileSerializer(serializers.ModelSerializer):
    images = images_serialzers.UserProfileImageSerializer(many=True)

    class Meta:
        model = models.User
        fields = (
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images'
        )


class ExploreUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
        )
