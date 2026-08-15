from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Client, Provider
from .permissions import IsClient, IsProvider, IsOwner, CanViewUserProfile
from .serializer import (ClientLoginSerializer, CustomClientDetailSerializer,
                         CustomProviderDetailSerializer,ProviderLoginSerializer,ClientRegisterSerializer,
                         ProviderRegisterSerializer)
from wine_collection_api.pagination import ProviderPagination

@extend_schema(tags=['Users - Clients'])
class ClientViewSet(viewsets.ModelViewSet):
    """Client view set."""
    serializer_class = CustomClientDetailSerializer
    pagination_class = None
    
    def get_queryset(self):
        return Client.objects.all()
    
    def get_permissions(self):
        """
        Docstring for get_permissions
        
        :param self: Description
        """
        if self.action in ['list','retrieve'] :
            return [IsClient()]
        elif self.action == 'create':
            return [IsAdminUser()]

        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsClient(), IsOwner()]
        
        return [IsClient()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsClient])
    def me(self, request):
        """Get current client details."""
        client = request.user.client
        serializer = self.get_serializer(client)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated, IsClient])
    def update_me(self, request):
        """Update current client details."""
        client = request.user.client
        serializer = self.get_serializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
@extend_schema(tags=['Users - Providers'])
class ProviderViewSet(viewsets.ModelViewSet):
    """Provider view set."""
    serializer_class = CustomProviderDetailSerializer
    pagination_class = ProviderPagination
    
    def get_queryset(self):
        """
        Docstring for get_queryset
        
        :param self: Description
        """
        return Provider.objects.all()

    def get_permissions(self):
        """
        Docstring for get_permissions
        
        :param self: Description
        """    
        if self.action == 'list':
            return [IsClient()]  # only clients can see provider list
        elif self.action == 'retrieve':
            return [CanViewUserProfile()]  # clients see all, providers see only their own
        elif self.action == 'create':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsProvider(), IsOwner()]  # only provider can modify their own
        return [IsProvider()]

    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsProvider])
    def me(self, request):
        """Get current provider details."""
        provider = request.user.provider
        serializer = self.get_serializer(provider)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated, IsProvider])
    def update_me(self, request):
        """Update current provider details."""
        provider = request.user.provider
        serializer = self.get_serializer(provider, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
@extend_schema(tags=['Auth'])
class ClientRegisterView(generics.CreateAPIView):
    """Client registration view."""
    serializer_class = ClientRegisterSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        """Create a new client."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        refresh = RefreshToken.for_user(client)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'client_type': 'client',
            'user': CustomClientDetailSerializer(client).data
        }, status=status.HTTP_201_CREATED)  
        
@extend_schema(tags=['Auth'])
class ProviderRegisterView(generics.CreateAPIView):
    """Provider registration view."""
    serializer_class = ProviderRegisterSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        """Create a new provider."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.save()
        refresh = RefreshToken.for_user(provider)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'client_type': 'provider',
            'user': CustomProviderDetailSerializer(provider).data
        }, status=status.HTTP_201_CREATED)
        
@extend_schema(tags=['Auth'])
class ClientLoginView(generics.GenericAPIView):
    """Client login view."""
    serializer_class = ClientLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Handle client login."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.validated_data['user']
        refresh = RefreshToken.for_user(client)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'client_type': 'client',
            'user': CustomClientDetailSerializer(client).data
        }, status=status.HTTP_200_OK)
        
        
@extend_schema(tags=['Auth'])
class ProviderLoginView(generics.GenericAPIView):
    """Provider login view."""
    serializer_class = ProviderLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Handle provider login."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data['user']
        refresh = RefreshToken.for_user(provider)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'client_type': 'provider',
            'user': CustomProviderDetailSerializer(provider).data
        }, status=status.HTTP_200_OK)
        