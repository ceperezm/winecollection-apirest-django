
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
import django_filters.rest_framework

from .models import Wine
from .serializer import (WineReadSerializer, WineWriteSerializer)
from .permissions import IsClient, IsProvider, IsProviderWineOwner
from wine_collection_api.pagination import StandardPagination
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Wines'])
class WineProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for providers to manage their own wines.
    """
    serializer_class = WineReadSerializer
    pagination_class = StandardPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['variety', 'harvest_year']
    search_fields = ['name', 'variety', 'maker']
    ordering_fields = ['name', 'harvest_year']

    def get_queryset(self):
        """Get queryset for providers wines."""
        return Wine.objects.filter(provider=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsProvider()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsProvider(), IsProviderWineOwner()]
        return [IsProvider()]

    def get_serializer_class(self):
        """Get serializer class based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return WineWriteSerializer
        return WineReadSerializer

@extend_schema(tags=['Wines'])
class WineClientViewSet(viewsets.ReadOnlyModelViewSet):
    """View set for clients to view wines."""
    serializer_class = WineReadSerializer
    pagination_class = StandardPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['variety', 'harvest_year', 'provider']

    def get_queryset(self):
        """Get queryset for wines."""
        return Wine.objects.all()

    def get_permissions(self):
        """Get permissions based on action."""
        if self.action in ['list', 'retrieve']:
            return [IsClient()]
        return [IsClient()]

from .filters import WineFilter

@extend_schema(tags=['Wines'])
class WinePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """Public view to list and retrieve wines."""
    queryset = Wine.objects.all()
    serializer_class = WineReadSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = WineFilter
    search_fields = ['name', 'variety', 'maker']
    ordering_fields = ['name', 'harvest_year', 'added_date']
                