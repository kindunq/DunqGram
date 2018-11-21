from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class Notifys(APIView):

    def get(self, request, format=None):
        user = request.user

        notifys = models.Notify.objects.filter(to=user)

        serializer = serializers.NotifySerializers(notifys, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
