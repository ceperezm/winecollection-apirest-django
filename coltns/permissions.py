from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    message = "User is not a client."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'client'))

class IsProvider(BasePermission):
    message = "User is not a provider."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'provider'))

class IsProviderCollectionOwner(BasePermission):
    message = "You do not own this provider collection."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(request.user, 'provider'):
            return obj.provider_id == request.user.id
        return False

class IsClientCollectionOwner(BasePermission):
    message = "You do not own this client collection."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(request.user, 'client'):
            return obj.client_id == request.user.id
        return False

class IsClientCollectionWineOwner(BasePermission):
    message = "You do not own this collection wine."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(request.user, 'client'):
            return obj.client_collection.client_id == request.user.id
        return False

class IsProviderCollectionWineOwner(BasePermission):
    message = "You do not own this provider collection wine."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(request.user, 'provider'):
            return obj.provider_collection.provider_id == request.user.id
        return False

class CanViewProviderCollection(BasePermission):
    """
    Permission to view provider collections based on user role.
    Clients can view all provider collections.
    Providers can only view their own provider collections.
    """
    message = "You do not have permission to view this collection."
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if hasattr(user, 'client') or hasattr(user, 'provider') or user.is_staff or user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'client'):
            return True
        if hasattr(user, 'provider'):
            return obj.provider_id == user.id
        return False