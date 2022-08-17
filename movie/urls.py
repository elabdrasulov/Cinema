from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("movies", MovieViewSet)
router.register("categories", CategoryViewSet)
router.register('comments', CommentViewSet)
# router.register("favorites", FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('toggle_like/<int:m_id>/', toggle_like),
    path('add_rating/<int:m_id>/', add_rating),
    path('add_to_favorite/<int:m_id>/', add_to_favorite),
    path('favorite/', FavoriteView.as_view()),
]