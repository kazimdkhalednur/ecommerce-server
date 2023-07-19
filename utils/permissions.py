from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Allows access only to seller.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "seller"
        )
