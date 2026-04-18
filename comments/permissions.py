from rest_framework import permissions
from users.models import Client, Provider

class CanViewComment(permissions.BasePermission):
    """Permission to check if the user can view a comment."""
    message = "User is not allowed to view this comment."
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if user is a Client
        try:
            Client.objects.get(user_ptr=user)
            return True
        except Client.DoesNotExist:
            pass

        # Check if user is a Provider
        try:
            Provider.objects.get(user_ptr=user)
            return True
        except Provider.DoesNotExist:
            pass

        return False    

