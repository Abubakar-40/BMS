from rest_framework.permissions import BasePermission


class IsStaffForRetrieveDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "DELETE"):
            return request.user.is_staff

        return True
