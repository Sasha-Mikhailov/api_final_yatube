from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CommentViewSet, PostViewSet

api_v1_router = DefaultRouter()
api_v1_router.register("posts", PostViewSet, basename="posts")
api_v1_router.register(
    r"posts/(?P<post_id>[\d]+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path(
        "v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("v1/", include(api_v1_router.urls)),
]
