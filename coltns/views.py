from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import Client, Provider

from .models import (
    ProviderCollection,
    ClientCollection,
    ClientCollectionWine,
    ProviderCollectionWine,
)

from .serializer import (
    ProviderCollectionReadSerializer,
    ProviderCollectionWriteSerializer,
    ClientCollectionReadSerializer,
    ClientCollectionWriteSerializer,
    ClientCollectionWineSerializer,
    ProviderCollectionWineSerializer,
)

from .permissions import (
    IsProvider,
    IsClient,
    IsProviderCollectionOwner,
    IsClientCollectionOwner,
    IsClientCollectionWineOwner,
    IsProviderCollectionWineOwner,
    CanViewProviderCollection,
)

from drf_spectacular.utils import extend_schema

# Provider collections
@extend_schema(tags=['Collections - Providers'])
class ProviderCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionReadSerializer

    def get_queryset(self):

        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollection.objects.none()

        if hasattr(user, 'client'):
            return ProviderCollection.objects.all()

        if hasattr(user, 'provider'):
            return ProviderCollection.objects.select_related('provider').filter(provider_id=user.id)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProviderCollection()]  # clients can see all collections, providers can view all but only modify their own
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsProvider(), IsProviderCollectionOwner()]  # only providers can modify their own
        return [IsAuthenticated()] 

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProviderCollectionWriteSerializer
        return ProviderCollectionReadSerializer

    def perform_create(self, serializer):
        # Serializer now handles User to Provider conversion
        serializer.save()

# Client collections
@extend_schema(tags=['Collections - Clients'])
class ClientCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ClientCollectionReadSerializer

    def get_queryset(self):
        return ClientCollection.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsClient()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsClient(), IsClientCollectionOwner()]
        return [IsClient()]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ClientCollectionWriteSerializer
        return ClientCollectionReadSerializer

    def perform_create(self, serializer):
        # Serializer now handles User to Client conversion
        serializer.save()

# Client collection wines
@extend_schema(tags=['Collections - Clients (Wines)'])
class ClientCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ClientCollectionWineSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ClientCollectionWine.objects.none()

        if hasattr(user, 'client'):
            return ClientCollectionWine.objects.filter(client_collection__client_id=user.id)

        if hasattr(user, 'provider'):
            return ClientCollectionWine.objects.none()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsClient()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsClient(), IsClientCollectionWineOwner()]
        return [IsClient()]


# Provider collection wines
@extend_schema(tags=['Collections - Providers (Wines)'])
class ProviderCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionWineSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollectionWine.objects.none()

        if hasattr(user, 'client'):
            return ProviderCollectionWine.objects.all()

        if hasattr(user, 'provider'):
            return ProviderCollectionWine.objects.filter(provider_collection__provider_id=user.id)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProviderCollection()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsProvider(), IsProviderCollectionWineOwner()]
        return [IsProvider()]
