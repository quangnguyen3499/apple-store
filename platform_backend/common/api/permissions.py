from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "User not a Admin."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        return False

class IsCustomer(BasePermission):
    message = "User not a Customer."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_customer:
            return True
        return False
