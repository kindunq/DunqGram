from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from dunqgram.users import models as user_models
from dunqgram.notify import views as notify_views
from dunqgram.users import serializers as user_serializers

class Feed(APIView):

    def get(self, request, format=None):
        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)


class LikeImage(APIView):

    def get(self, request, id, format=None):
        
        # 1. id crawling in like models

        likes = models.Like.objects.filter(image__id=id)

        # 2. create array of creator

        like_creators_ids = likes.values('creator_id')

        # 3. creatorid find in user model

        users = user_models.User.objects.filter(id__in=like_creators_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # create notification for like

    def post(self, request, id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )

            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

        notify_views.create_notify(user, found_image.creator, 'like', found_image  )

        new_like.save()
        

        return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):
    def delete(self, request, id, format=None):
        user = request.user
        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentOnImage(APIView):

    # comment notification

    def post(self, request, id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)
            

            notify_views.create_notify(user, found_image.creator, 'comment',found_image, serializer.data['message'] )

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, id, formant=None):
        user = request.user
        try:
            found_comment = models.Comment.objects.get(id=id, creator=user)
            found_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):
    def get(self, request, format=None):
        hashtags = request.query_params.get('hashtags', None)

        hashtags = hashtags.split(",")

        if hashtags is not None:
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_404_NOT_FOUND)


class ModerateComments(APIView):

    def delete(self, request, id, comment_id, format=None):

        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(APIView):

    def find_own_image(self, id, user):
        try:
            image = models.Image.objects.get(id=id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None


    def get(self, request, id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = serializers.ImageSerializer(image)

        return Response(data=serializer.data, status= status.HTTP_200_OK)

    def put(self, request, id, format=None):
        
        user = request.user

        image = self.find_own_image(id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)
       
        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else :

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
       
        user = request.user

        image = self.find_own_image(id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
