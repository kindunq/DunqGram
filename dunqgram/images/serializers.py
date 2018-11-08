from rest_framework import serializers
from . import models
from dunqgram.users import models as user_models

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = "__all__"


class FeedUserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = user_models.User
        fields = (
            'username', 'profile_image'
            )


class ImageSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    creator = FeedUserSerializer(many=True)

    class Meta:
        model = models.Image
        fields = ("id", "file", "location", "caption", "comments", "likes", "creator")

