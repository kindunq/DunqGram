from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from dunqgram.notify import views as notify_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class ExploreUsers(APIView):
    def get(self, request, format=None):

        last_five = models.User.objects.all().exclude(username='admin').order_by('date_joined')[:5]
        serializer = serializers.ListUserSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):

    # follow notification

    def post(self, request, id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)

        user.save()

        notify_views.create_notify(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    def post(self, request, id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)

        user.save()

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get_user(self, username):

        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format=None):

        found_user = self.get_user(username)

        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):

        user = request.user

        found_user = self.get_user(username)

        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        elif found_user.username != user.username:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:

            serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)

            # partial=True required ignoring

            if serializer.is_valid():

                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_200_OK)

            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowers(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username', None)

        if username is not None:

            users = models.User.objects.filter(username__icontains=username)

            serializer = serializers.ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    def put(self, request, username, format=None):

        user = request.user  # user check

        if user.username == username:

            current_password = request.data.get('current_password', None)  # password check

            if current_password is not None:

                passwords_match = user.check_password(current_password)  # password check

                if passwords_match:

                    new_password = request.data.get('new_password', None)  # new password check

                    if new_password is not None:

                        user.set_password(new_password)  # set password

                        user.save()  # save password

                        return Response(status=status.HTTP_200_OK)

                    else:

                        return Response(status=status.HTTP_400_BAD_REQUEST)

                else:

                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:

            return Response(status=status.HTTP_401_UNAUTHORIZED)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
