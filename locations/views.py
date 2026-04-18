from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializer import CountrySerializer, CitySerializer
from .models import Country, City


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for countries"""
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [IsAdminUser]  
    
class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view for cities"""
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [IsAdminUser] 
