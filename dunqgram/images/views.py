from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class Feed(APIView):

    def get(self, request, format=None):
        
        user = request.user

        following_users = user.following.all()

        for following_users in following_users
            print(following_users.images.all())

        return Response(status=200)