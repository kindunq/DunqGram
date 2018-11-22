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

def create_notify(creator, to,  notify_type, image = None , comment = None):

    print(creator, to,  notify_type, image, comment)

    notify = models.Notify.objects.create(
        creator = creator,
        to=to,
        notify_type = notify_type,
        image = image,
        comment = comment,
    )

    notify.save()

