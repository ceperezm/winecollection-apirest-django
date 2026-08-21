
from users.permissions import IsClient, IsOwner
from users.models import Provider, Client
from .permissions import CanViewComment
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, serializers
import django_filters.rest_framework
from wine_collection_api.pagination import CommentPagination
from drf_spectacular.utils import extend_schema

from .models import WineComment, ClientCollectionComment, ProviderCollectionComment
from .serializer import (WineCommentReadSerializer,WineCommentWriteSerializer,
ClientCollectionReadCommentSerializer,ClientCollectionWriteCommentSerializer,
ProviderCollectionReadCommentSerializer, ProviderCollectionWriteCommentSerializer
)


# Wine comments
@extend_schema(tags=['Comments - Wines'])
class WineCommentViewSet(viewsets.ModelViewSet):
    pagination_class = CommentPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['wine']

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return WineComment.objects.none()

        # Check if user is a Client by looking for Client instance
        try:
            Client.objects.get(user_ptr=user)
            return WineComment.objects.select_related('wine', 'client')
        except Client.DoesNotExist:
            pass

        # Check if user is a Provider by looking for Provider instance
        try:
            Provider.objects.get(user_ptr=user)
            return WineComment.objects.filter(wine__provider=user).select_related('wine', 'client')
        except Provider.DoesNotExist:
            pass

        return WineComment.objects.none()

    def get_permissions(self):
        """
        Returns the list of permissions depending on the action being performed.

        :param self: ViewSet instance
        """
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [CanViewComment()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsClient(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WineCommentWriteSerializer
        return WineCommentReadSerializer

    def perform_create(self, serializer):
        # Serializer now handles User to Client conversion
        serializer.save()

@extend_schema(tags=['Comments - Client Collections'])
class ClientCollectionCommentViewSet(viewsets.ModelViewSet):
    queryset = ClientCollectionComment.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['collection']

    def get_permissions(self):
        """
        Returns the list of permissions depending on the action being performed.

        :param self: ViewSet instance
        """
        if self.action in ['list', 'retrieve']:
            return [IsClient()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsClient(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientCollectionWriteCommentSerializer
        return ClientCollectionReadCommentSerializer

    def perform_create(self, serializer):
        # Serializer now handles User to Client conversion
        serializer.save()

@extend_schema(tags=['Comments - Provider Collections'])
class ProviderCollectionCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['collection']

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return ProviderCollectionComment.objects.none()

        # Check if user is a Client by looking for Client instance
        try:
            Client.objects.get(user_ptr=user)
            return ProviderCollectionComment.objects.select_related('collection', 'client')
        except Client.DoesNotExist:
            pass

        # Check if user is a Provider by looking for Provider instance
        try:
            Provider.objects.get(user_ptr=user)
            # Provider can only see comments on their own collections
            return ProviderCollectionComment.objects.filter(collection__provider=user).select_related('collection', 'client')
        except Provider.DoesNotExist:
            pass

        return ProviderCollectionComment.objects.none()

    def get_permissions(self):
        """
        Returns the list of permissions depending on the action being performed.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsClient(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProviderCollectionWriteCommentSerializer
        return ProviderCollectionReadCommentSerializer

    def perform_create(self, serializer):
        # Serializer now handles User to Client conversion
        serializer.save()