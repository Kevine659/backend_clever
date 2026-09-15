from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    message = "Vous devez être administrateur pour accéder à cette ressource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )