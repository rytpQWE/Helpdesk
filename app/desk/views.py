from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from desk.models import Desk
from desk.pagination import MainDeskPagination, AdminDeskPagination
from desk.serializers import DeskCreateSerializer, AdminDeskSerializer


class DeskViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Desk.objects.all()
    serializer_class = DeskCreateSerializer

    def perform_create(self, serializer):
        """Create and save current user in form(desk)"""
        serializer.save(User=self.request.user)

    def get_queryset(self):
        """Get object's current user"""
        return self.queryset.filter(User=self.request.user.id)


class AdminDeskViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,):
    permission_classes = [IsAdminUser]
    queryset = Desk.objects.all().order_by('created_at')[:3]
    serializer_class = AdminDeskSerializer

