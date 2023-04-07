from django.core.mail import EmailMessage
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
    pagination_class = MainDeskPagination
    """To delete desk, you need to pass pk in url"""

    def perform_create(self, serializer):
        """Create and save current user in form(desk)"""
        serializer.save(User=self.request.user)

    def get_queryset(self):
        """Get object's current user"""
        return self.queryset.filter(User=self.request.user.id)


class AdminDeskViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin):
    """To update desk, you need to pass pk in url"""
    permission_classes = [IsAdminUser]
    # Ordering only Accepted application
    queryset = Desk.objects.filter(status='accepted').order_by('created_at')
    serializer_class = AdminDeskSerializer
    pagination_class = AdminDeskPagination

    def perform_update(self, serializer):
        obj = serializer.save()
        email = EmailMessage(
            'HelpDesk',
            f'Your application: {obj.title} has been completed',
            to=[str(obj.User.email)]
        )
        email.send()
        return obj

