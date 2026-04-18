
from rest_framework import serializers
from .models import WineComment, ClientCollectionComment
from users.models import Client

class WineCommentReadSerializer(serializers.ModelSerializer):
    """Serializer for reading wine comments."""

    client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    wine = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = WineComment
        
        fields = [
            'id', # Primary key
            'client', # Who made the comment
            'wine', # Foreign key to Wine
            'comment', # Comment text
            'comment_date', # Comment date
        ]
        read_only_fields = fields

class WineCommentWriteSerializer(serializers.ModelSerializer):
    """Serializer for writing wine comments."""

    class Meta:
        model = WineComment
        fields =[
            'wine','comment'
        ]

    def validate_comment(self,value):
        if len(value) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters long.")
        return value

    def validate(self, data):
        return data
    
    def create(self, validated_data):
        # Convert User to Client instance
        request = self.context.get('request')
        user = request.user
        client_instance = Client.objects.get(user_ptr=user)
        
        # Create comment with the correct client instance
        validated_data['client'] = client_instance
        return super().create(validated_data)   


class ClientCollectionReadCommentSerializer(serializers.ModelSerializer):
    """Serializer for reading client collection comments."""

    client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    collection = serializers.SlugRelatedField(slug_field='collection_name', read_only=True)

    class Meta:
        model = ClientCollectionComment
        
        fields = [
            'id',
            'client', # Client who made the comment
            'collection',
            'comment',
            'comment_date',
        ]
        read_only_fields = fields

class ClientCollectionWriteCommentSerializer(serializers.ModelSerializer):
    """ Serializer for writing client collection comments."""

    class Meta:
        model = ClientCollectionComment
        fields = ['collection','comment']

    def validate_comment(self,value):
            if len(value) < 5:
                raise serializers.ValidationError("Comment must be at least 5 characters long.")
            return value

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        collection = data.get('collection')
        
        # Compare user_ptr IDs since user is User and collection.client is Client
        if user.id == collection.client.user_ptr_id:
            raise serializers.ValidationError(
                "Client cannot comment on their own collection."
            )
        return data
    
    def create(self, validated_data):
        # Convert User to Client instance
        request = self.context.get('request')
        user = request.user
        client_instance = Client.objects.get(user_ptr=user)
        
        # Create comment with the correct client instance
        validated_data['client'] = client_instance
        return super().create(validated_data)
