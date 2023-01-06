from rest_framework import generics, permissions

from .models import Master
from .serializers import MasterSerializer


class WantsView(generics.ListAPIView):
    """
    View that for listing and creating all capacity templates of a user.
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
