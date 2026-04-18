from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'providers', views.ProviderViewSet, basename='provider')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include([
        path("register/client/", views.ClientRegisterView.as_view(), name="client-register"),
        path("register/provider/", views.ProviderRegisterView.as_view(), name="provider-register"),
        path("login/client/", views.ClientLoginView.as_view(), name="client-login"),
        path("login/provider/", views.ProviderLoginView.as_view(), name="provider-login"),
    ])),
]