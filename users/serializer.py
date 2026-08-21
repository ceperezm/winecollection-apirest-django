from rest_framework import serializers
from .models import User, Client, Provider
from locations.models import City
from django.contrib.auth.password_validation import validate_password


class CustomClientDetailSerializer(serializers.ModelSerializer):
    """Serializer view and edit for clients."""
    class Meta:
        model = Client
        fields = ['id', 'username', 'first_name', 'last_name', 'birth_date', 'registration_date', 'email', 'is_active']
        read_only_fields = ['id','first_name', 'last_name','registration_date','is_active']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user.id != instance.id:
                ret.pop('email', None)
                ret.pop('birth_date', None)
        else:
            ret.pop('email', None)
            ret.pop('birth_date', None)
        return ret
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user is already registered with this username.")
        return value       
        
    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            return value
        if Client.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return value
        
                
class CustomProviderDetailSerializer(serializers.ModelSerializer):
    """Serializer view and edit for providers."""
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = Provider
        fields = ['id', 'name', 'description', 'phone_number', 'identifier_number', 'city', 'registration_date', 'email', 'is_active']
        read_only_fields = ['id','identifier_number','registration_date','is_active']
     
    def validate_name(self,value):
        if self.instance and self.instance.name == value:
            return value
        if Provider.objects.filter(name=value).exists():
            raise serializers.ValidationError("A user is already registered with this name.")
        return value      

    def validate_email(self, value):
        if self.instance and self.instance.email == value:
            return value
        if Provider.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return value

class ClientLoginSerializer(serializers.Serializer):
    """Serializer for client login."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        try:
            client = Client.objects.get(username=username)
        except Client.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No client found with this username.'})
        if not client.check_password(password):
            raise serializers.ValidationError({'detail': 'Incorrect password.'})
        if not client.is_active:
            raise serializers.ValidationError({'detail': 'Client account is disabled.'})
        data['user'] = client
        return data
            
    
class ProviderLoginSerializer(serializers.Serializer):
    """Serializer for provider login."""
    identifier_number = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        identifier_number = data.get('identifier_number')
        password = data.get('password')
        
        try:
            provider = Provider.objects.get(identifier_number=identifier_number)
        except Provider.DoesNotExist:
            raise serializers.ValidationError({'detail': 'No provider found with this identifier number.'})
        if not provider.check_password(password):
            raise serializers.ValidationError({'detail': 'Incorrect password.'})
        if not provider.is_active:
            raise serializers.ValidationError({'detail': 'Provider account is disabled.'})
        data['user'] = provider
        return data
    
    
 # For client registration   
class ClientRegisterSerializer(serializers.ModelSerializer):
    """Register for new clients."""   
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                      style={'input_type': 'password'},label='Password')
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'},label='Confirm Password')
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'birth_date', 'email', 'password1', 'password2']
        extra_kwargs = {
            'username': {'required': True},'first_name': {'required': True},'last_name': {'required': True},'email': {'required': True},'birth_date': {'required': True},
        }
        
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user is already registered with this username.")
        return value        
        
    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return value
        
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data
        
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        client = Client(**validated_data)
        client.set_password(password)
        client.save()
        return client
                 
           
# For provider registration 

class ProviderRegisterSerializer(serializers.ModelSerializer):
    """Register for new providers."""   
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                      style={'input_type': 'password'},label='Password')
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'},label='Confirm Password')
    class Meta:
        model = Provider
        fields = ['name', 'description', 'phone_number', 'identifier_number', 'city', 'email', 'password1', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'description': {'required': True},
            'phone_number': {'required': True},
            'identifier_number': {'required': True},
            'city': {'required': True},
        }

    def validate_name(self,value):
        if not value:
            return value
        if Provider.objects.filter(name=value).exists():
            raise serializers.ValidationError("A user is already registered with this name.")
        return value

    def validate_identifier_number(self,value):
        if not value:
            return value
        if Provider.objects.filter(identifier_number=value).exists():
            raise serializers.ValidationError("A user is already registered with this identifier number.")
        return value

    def validate_email(self, value):
        if not value:
            return value
        if Provider.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return value
        
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data
        
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        provider = Provider(**validated_data)
        provider.username = validated_data.get('email') # Use email as username
        provider.set_password(password)
        provider.save()
        return provider