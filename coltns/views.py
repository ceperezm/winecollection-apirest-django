from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import Client, Provider
import django_filters.rest_framework
from rest_framework import filters
from django.db.models import Count

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

from wine_collection_api.pagination import CollectionPagination
from drf_spectacular.utils import extend_schema

# Provider collections
@extend_schema(tags=['Collections - Providers'])
class ProviderCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionReadSerializer
    pagination_class = CollectionPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['provider']
    search_fields = ['collection_name', 'description']
    ordering_fields = ['registration_date', 'collection_name', 'wines_count']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollection.objects.none()
        
        queryset = ProviderCollection.objects.annotate(wines_count=Count('providercollectionwine'))
        if hasattr(user, 'client'):
            return queryset.filter(is_public=True)
        if hasattr(user, 'provider'):
            return queryset.select_related('provider').filter(provider_id=user.id)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProviderCollection()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsProvider(), IsProviderCollectionOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProviderCollectionWriteSerializer
        return ProviderCollectionReadSerializer

    def perform_create(self, serializer):
        serializer.save()

# Client collections
@extend_schema(tags=['Collections - Clients'])
class ClientCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ClientCollectionReadSerializer
    pagination_class = CollectionPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['collection_name', 'description']
    ordering_fields = ['registration_date', 'collection_name', 'wines_count']

    def get_queryset(self):
        """Returns the client collections (all if client, none if provider)."""
        user = self.request.user
        if not user.is_authenticated or hasattr(user, 'provider'):
            return ClientCollection.objects.none()
        
        return ClientCollection.objects.filter(client_id=user.id).annotate(wines_count=Count('clientcollectionwine'))

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
        serializer.save()

# Client collection wines — no pagination, filtered by collection
@extend_schema(tags=['Collections - Clients (Wines)'])
class ClientCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ClientCollectionWineSerializer
    pagination_class = None
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['client_collection']

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


# Provider collection wines — no pagination, filtered by collection
@extend_schema(tags=['Collections - Providers (Wines)'])
class ProviderCollectionWineViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderCollectionWineSerializer
    pagination_class = None
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['provider_collection']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProviderCollectionWine.objects.none()
        if hasattr(user, 'client'):
            return ProviderCollectionWine.objects.filter(provider_collection__is_public=True)
        if hasattr(user, 'provider'):
            return ProviderCollectionWine.objects.filter(provider_collection__provider_id=user.id)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [CanViewProviderCollection()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsProvider(), IsProviderCollectionWineOwner()]
        return [IsProvider()]
