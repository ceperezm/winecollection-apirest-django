"""
URL configuration for wine_collection_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import OpenAPIRenderer, JSONOpenAPIRenderer

schema_view = get_schema_view(
    title="Wine collection API",
    description="API Documentation for Wine Collection Application",
    version="1.0.0",
    public=True,
    renderer_classes=[OpenAPIRenderer, JSONOpenAPIRenderer],
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('coltns/',include('coltns.urls')),
    path('wines/',include('wines.urls')),
    path('users/',include('users.urls')),
    path('comments/',include('comments.urls')),
    path('', include('locations.urls')),
]
