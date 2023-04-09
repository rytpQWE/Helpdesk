from rest_framework.permissions import BasePermission


class IsEmployeeUser(BasePermission):
    """
    Allows access only to employee users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.employee.is_employee or request.user.is_staff)

