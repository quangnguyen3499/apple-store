from rest_framework.permissions import BasePermission


class IsCommunityLeader(BasePermission):
    message = "User not a Community Leader."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_cl:
            return True
        return False


class IsSuki(BasePermission):
    message = "User not a Suki."

    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.user.is_suki:
            return True
        return False
