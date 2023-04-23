from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from desk.models import Desk
from desk.pagination import MainDeskPagination, AdminDeskPagination
from desk.permissions import IsEmployeeUser
from desk.serializers import DeskCreateSerializer, EmployeeDeskSerializer, DeskCompleteSerializer
from desk.tasks import send_mail_for_user, send_employee_mail


class DeskViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Desk.objects.order_by('-id')
    serializer_class = DeskCreateSerializer
    pagination_class = MainDeskPagination
    """
    To delete desk, you need to pass pk in url
    """

    def perform_create(self, serializer):
        """
        Create and save current user in form(desk)
        """
        obj = serializer.save(User=self.request.user)
        send_employee_mail.delay(obj.id)

    def get_queryset(self):
        """
        Get object's current user
        """
        return self.queryset.filter(User=self.request.user.id)


class DeskCompleteViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Desk.objects.filter(status='completed').order_by('-id')
    serializer_class = DeskCompleteSerializer
    pagination_class = MainDeskPagination

    def get_queryset(self):
        """
        Get object's current user
        """
        return self.queryset.filter(User=self.request.user.id)


class AdminDeskViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin):
    """
    To update desk, you need to pass pk in url
    """
    permission_classes = [IsEmployeeUser]
    # Ordering only Accepted application
    queryset = Desk.objects.filter(status='accepted').order_by('-id')
    serializer_class = EmployeeDeskSerializer
    pagination_class = AdminDeskPagination

    def perform_update(self, serializer):
        obj = serializer.save()
        send_mail_for_user.delay(obj.id)
        return obj

