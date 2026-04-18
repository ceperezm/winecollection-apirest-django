from rest_framework import serializers
from .models import Country, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']
        read_only_fields = ['id']
        
class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True, source='country_id')
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        required=True,
        write_only=True
    )
    
    class Meta:
        model = City
        fields = ['name', 'country', 'country_id']