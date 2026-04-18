from rest_framework.permissions import BasePermission
from users.models import Client, Provider

class IsClient(BasePermission):
    message = "User is not a client."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            Client.objects.get(user_ptr=request.user)
            return True
        except Client.DoesNotExist:
            return False

class IsProvider(BasePermission):
    message = "User is not a provider."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            Provider.objects.get(user_ptr=request.user)
            return True
        except Provider.DoesNotExist:
            return False

class IsProviderCollectionOwner(BasePermission):
    message = "You do not own this provider collection."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            Provider.objects.get(user_ptr=request.user)
            return obj.provider.user_ptr_id == request.user.id
        except Provider.DoesNotExist:
            return False

class IsClientCollectionOwner(BasePermission):
    message = "You do not own this client collection."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            Client.objects.get(user_ptr=request.user)
            return obj.client.user_ptr_id == request.user.id
        except Client.DoesNotExist:
            return False

class IsClientCollectionWineOwner(BasePermission):
    message = "You do not own this collection wine."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            Client.objects.get(user_ptr=request.user)
            return obj.client_collection.client.user_ptr_id == request.user.id
        except Client.DoesNotExist:
            return False

class IsProviderCollectionWineOwner(BasePermission):
    message = "You do not own this provider collection wine."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            Provider.objects.get(user_ptr=request.user)
            return obj.provider_collection.provider.user_ptr_id == request.user.id
        except Provider.DoesNotExist:
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
        if not user.is_authenticated:
            return False
        # Check if user is Client or Provider
        try:
            Client.objects.get(user_ptr=user)
            return True
        except Client.DoesNotExist:
            pass
        try:
            Provider.objects.get(user_ptr=user)
            return True
        except Provider.DoesNotExist:
            pass
        if user.is_staff or user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Check if user is Client
        try:
            Client.objects.get(user_ptr=user)
            return True
        except Client.DoesNotExist:
            pass
        # Check if user is Provider
        try:
            Provider.objects.get(user_ptr=user)
            return obj.provider.user_ptr_id == user.id
        except Provider.DoesNotExist:
            pass
        return False