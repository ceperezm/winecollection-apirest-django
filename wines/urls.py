from django.urls import path, include
from rest_framework import routers
from wines import views


router = routers.DefaultRouter()
router.register(r'provider-wines', views.WineProviderViewSet, 'provider-wines')
router.register(r'client-wines', views.WineClientViewSet, 'client-wines')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/public-wines/", views.WinePublicListView.as_view(), name='public-wines'),
]
