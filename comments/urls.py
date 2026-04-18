from django.urls import path, include
from rest_framework import routers
from comments import views

router = routers.DefaultRouter()
router.register(r'wine-comment',views.WineCommentViewSet,'wine-comment')
router.register(r'client-collection-comment',views.ClientCollectionCommentViewSet,'client-collection-comment')

urlpatterns = [
    path("api/v1/", include(router.urls))
]