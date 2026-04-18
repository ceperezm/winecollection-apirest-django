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

# Provider collections
class ProviderCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionReadSerializer

    def get_queryset(self):

        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollection.objects.none()

        if isinstance(user, Client):
            return ProviderCollection.objects.all()

        if isinstance(user, Provider):
            return ProviderCollection.objects.select_related('provider').filter(provider=user)

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
class ClientCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ClientCollectionWineSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ClientCollectionWine.objects.none()

        if isinstance(user, Client):
            return ClientCollectionWine.objects.all()

        if isinstance(user, Provider):
            return ClientCollectionWine.objects.none()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsClient()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsClient(), IsClientCollectionWineOwner()]
        return [IsClient()]


# Provider collection wines
class ProviderCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionWineSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollectionWine.objects.none()

        if isinstance(user, Client):
            return ProviderCollectionWine.objects.all()

        if isinstance(user, Provider):
            return ProviderCollectionWine.objects.filter(provider_collection__provider=user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProviderCollection()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsProvider(), IsProviderCollectionWineOwner()]
        return [IsProvider()]
