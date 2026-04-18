from django.urls import path, include
from rest_framework import routers
from locations import views

router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet, 'cities')
router.register(r'countries', views.CountryViewSet, 'countries')

urlpatterns = [
    path("api/v1/",include(router.urls))
]