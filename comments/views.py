
from users.permissions import IsClient, IsOwner
from users.models import Provider, Client
from .permissions import CanViewComment
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, serializers


from .models import WineComment, ClientCollectionComment
from .serializer import (WineCommentReadSerializer,WineCommentWriteSerializer,
ClientCollectionReadCommentSerializer,ClientCollectionWriteCommentSerializer
)

# Wine comments

class WineCommentViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return WineComment.objects.none()

        # Check if user is a Client by looking for Client instance
        try:
            Client.objects.get(user_ptr=user)
            return WineComment.objects.select_related('wine','client')
        except Client.DoesNotExist:
            pass

        # Check if user is a Provider by looking for Provider instance
        try:
            Provider.objects.get(user_ptr=user)
            return WineComment.objects.filter(wine__provider=user).select_related('wine','client')
        except Provider.DoesNotExist:
            pass

        return WineComment.objects.none()

    def get_permissions(self):
        """
        Docstring for get_permissions
        
        :param self: Description
        """
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [CanViewComment()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsClient(),IsOwner()]
        return [IsAuthenticated()]


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WineCommentWriteSerializer
        return WineCommentReadSerializer
    def perform_create(self,serializer):
        # Serializer now handles User to Client conversion
        serializer.save()
            
    
class ClientCollectionCommentViewSet(viewsets.ModelViewSet):
    queryset = ClientCollectionComment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Docstring for get_permissions
        
        :param self: Description
        """
        if self.action in ['list','retrieve']:
            return [IsClient()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsClient(),IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientCollectionWriteCommentSerializer
        return ClientCollectionReadCommentSerializer


    def perform_create(self, serializer):
        # Serializer now handles User to Client conversion
        serializer.save()