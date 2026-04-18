from rest_framework import serializers
from .models import ClientCollection,ProviderCollection,ClientCollectionWine,ProviderCollectionWine,Type
from wines.serializer import WineReadSerializer, WineWriteSerializer
from wines.models import Wine
from users.models import User, Client, Provider

class TypeSerializer(serializers.ModelSerializer):
    """Serializer for Type model."""
    class Meta:
        model = Type
        fields = ['id', 'type_name', 'description']
        read_only_fields = ['id']
        
class ProviderCollectionReadSerializer(serializers.ModelSerializer):
    """Serializer for reading ProviderCollection data."""
    type = TypeSerializer(read_only=True)
    provider = serializers.SlugRelatedField(slug_field='username', read_only=True)
    wines_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ProviderCollection
        fields = ['id', 'collection_name', 'description', 'registration_date', 'provider', 'type', 'wines_count']
    def get_wines_count(self, obj):
        return obj.providercollectionwine_set.count()
        
class ProviderCollectionWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating ProviderCollection data."""
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(),
        source='type',
        write_only=True
    )
    
    
    class Meta:
        model = ProviderCollection
        fields = ['id', 'collection_name', 'description', 'provider_id', 'type_id', 'registration_date']
        read_only_fields = ['id', 'registration_date']
        
    def validate_collection_name(self, value):
        """Validate name collection."""
        if not value or not value.strip():
            raise serializers.ValidationError("Collection name cannot be empty.")
        if ProviderCollection.objects.filter(collection_name=value).exists():
            raise serializers.ValidationError("Collection name already exists.")
        return value
    
    def create(self, validated_data):
        # Convert User to Provider instance
        request = self.context.get('request')
        user = request.user
        provider_instance = Provider.objects.get(user_ptr=user)
        
        # Create collection with the correct provider instance
        validated_data['provider'] = provider_instance
        return ProviderCollection.objects.create(**validated_data)
        
        
class ClientCollectionReadSerializer(serializers.ModelSerializer):
    """Serializer for reading ClientCollection data."""
    client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    wines_count = serializers.SerializerMethodField()
    class Meta:
        model = ClientCollection
        fields = ['id', 'collection_name', 'description', 'registration_date', 'client', 'wines_count']
        
    def get_wines_count(self, obj):
        return obj.clientcollectionwine_set.count()
        
class ClientCollectionWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating ClientCollection data."""
        
    class Meta:
        model = ClientCollection
        fields = ['id', 'collection_name', 'description', 'client_id', 'registration_date']
        read_only_fields = ['id', 'registration_date']
        
    def validate_collection_name(self, value):
        """Validate name collection."""
        if not value or not value.strip():
            raise serializers.ValidationError("Collection name cannot be empty.")
        if ClientCollection.objects.filter(collection_name=value).exists():
            raise serializers.ValidationError("Collection name already exists.")
        return value
    
    def create(self, validated_data):
        # Convert User to Client instance
        request = self.context.get('request')
        user = request.user
        client_instance = Client.objects.get(user_ptr=user)
        
        # Create collection with the correct client instance
        validated_data['client'] = client_instance
        return ClientCollection.objects.create(**validated_data)    
        
class ClientCollectionWineSerializer(serializers.ModelSerializer):
    """Serializer for ClientCollectionWine model."""
    wine = WineReadSerializer(read_only=True)
    client_collection = serializers.SlugRelatedField(slug_field='collection_name', read_only=True)
    wine_id = serializers.PrimaryKeyRelatedField(
        queryset=Wine.objects.all(),
        source='wine',
        write_only=True
    )
    client_collection_id = serializers.PrimaryKeyRelatedField(
        queryset=ClientCollection.objects.all(),
        source='client_collection',
        write_only=True
    )
    
    class Meta:
        model = ClientCollectionWine
        fields = ['id', 'client_collection', 'wine', 'wine_id', 'client_collection_id', 'added_date']
        read_only_fields = ['id', 'added_date', 'client_collection', 'wine']
        
    def validate(self, data): 
        wine = data.get('wine')
        client_collection = data.get('client_collection')
        
        if wine and client_collection:
            if ClientCollectionWine.objects.filter(wine=wine, client_collection=client_collection).exists():
                raise serializers.ValidationError("This wine is already in the client's collection.")
        
        return data
        
class ProviderCollectionWineSerializer(serializers.ModelSerializer):
    """Serializer for ProviderCollectionWine model."""
    wine = WineReadSerializer(read_only=True)
    provider_collection = serializers.SlugRelatedField(slug_field='collection_name', read_only=True)
    wine_id = serializers.PrimaryKeyRelatedField(
        queryset=Wine.objects.all(),
        source='wine',
        write_only=True
    )
    provider_collection_id = serializers.PrimaryKeyRelatedField(
        queryset=ProviderCollection.objects.all(),
        source='provider_collection',
        write_only=True
    )
    
    class Meta:
        model = ProviderCollectionWine
        fields = ['id', 'provider_collection', 'wine', 'wine_id', 'provider_collection_id', 'added_date']
        read_only_fields = ['id', 'added_date', 'provider_collection', 'wine']
     
    def validate(self, data): # Validate no duplicate wines in the same collection
        wine = data.get('wine')
        provider_collection = data.get('provider_collection')
        
        if wine and provider_collection:
            if ProviderCollectionWine.objects.filter(wine=wine, provider_collection=provider_collection).exists():
                raise serializers.ValidationError("This wine is already in the provider's collection.")
        
        return data