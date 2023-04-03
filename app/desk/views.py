from rest_framework import viewsets, mixins

from desk.models import Desk
from desk.serializers import DeskCreateSerializer


class DeskViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  ):
    queryset = Desk.objects.all()
    serializer_class = DeskCreateSerializer

    def perform_create(self, serializer):
        """Create and save current user in form(desk)"""
        serializer.save(User=self.request.user)

    def get_queryset(self):
        """Get object's current user"""
        return self.queryset.filter(user=self.request.user)
