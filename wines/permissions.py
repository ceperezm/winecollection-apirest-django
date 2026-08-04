from rest_framework.permissions import BasePermission


class IsClient(BasePermission):
    """
    Allows access only to users with role 'client'.
    """
    message = "User is not a client to access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'client')
        )


class IsProvider(BasePermission):
    """
    Allows access only to users with role 'provider'.
    """
    message = "User is not a provider to access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'provider')
        )


class IsProviderWineOwner(BasePermission):
    """
    Object-level permission to allow providers to manage only their own wines.
    Staff and superusers are always allowed.
    """
    message = "You do not own this wine."

    def has_object_permission(self, request, view, obj):
        # Admin override
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Object must be a Wine instance
        return (
            request.user
            and request.user.is_authenticated
            and obj.provider_id == request.user.id
        )