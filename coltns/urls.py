from django.urls import path, include
from rest_framework import routers
from coltns import views

router = routers.DefaultRouter()
router.register(r'provider-collection', views.ProviderCollectionViewSet, 'provider-collection')
router.register(r'client-collection', views.ClientCollectionViewSet, 'client-collection')
router.register(r'client-collection-wine', views.ClientCollectionWineViewSet, 'client-collection-wine')
router.register(r'provider-collection-wine', views.ProviderCollectionWineViewSet, 'provider-collection-wine')


urlpatterns = [
    path("api/v1/", include(router.urls))
]
