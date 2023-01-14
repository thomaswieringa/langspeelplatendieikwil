from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Master
from .serializers import MasterSerializer

import requests

class WantsView(generics.ListAPIView):
    """
    View that listing all wants of a user
    """
    serializer_class = MasterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Master.objects.filter(user=user)


class WantDelete(generics.DestroyAPIView):
    """
    View that deleting a want by its id
    """
    serializer_class = MasterSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Master.objects.all()


class AddMaster(APIView):
    """
    View that takes a master id and uses the discogs API to create a full Master model to save to db
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, master_id):
        response = requests.get('https://api.discogs.com/masters/{}'.format(master_id)).json()
        if 'id' not in response.keys():
            return Response('Could not find master')
        else:
            master = Master(master_id=master_id,
                            title=response['title'],
                            artist=response['artists'][0]['name'],
                            genre=response['genres'][0],
                            year=response['year'],
                            discogs_url=response['uri'],
                            user=request.user
            )
            master.save()
            return Response("added master succesfully!!")

# #   master_id = models.IntegerField()
#     title = models.CharField(max_length=100)
#     artist = models.CharField(max_length=100)
#     genre = models.CharField(max_length=100)
#     year = models.IntegerField()
#     discogs_url = models.CharField(max_length=100)
#     image_url = models.CharField(max_length=100)
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )