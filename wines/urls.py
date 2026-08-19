from django.urls import path, include
from rest_framework import routers
from .views import WineProviderViewSet, WineClientViewSet, WinePublicViewSet

router = routers.DefaultRouter()
router.register(r'provider-wine', WineProviderViewSet, basename='provider-wine')
router.register(r'client-wine', WineClientViewSet, basename='client-wine')
router.register(r'public-wines', WinePublicViewSet, basename='public-wines')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
