from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import Master
from .serializers import MasterSerializer


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


class StartScraping(APIView):
    """
    View that deleting a want by its id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        # start scraping process
        print("ewa")