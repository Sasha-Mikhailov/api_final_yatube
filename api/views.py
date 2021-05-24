from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, permissions, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend

from .models import Follow, Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

User = get_user_model()


class GetPostViewSetTemplate(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """
      A viewset that provides default `create()` and `list()` and  actions.
    """
    pass


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs["post_id"])

    def get_queryset(self):
        post = self.get_post()
        queryset = post.comments

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(GetPostViewSetTemplate):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class FollowViewSet(GetPostViewSetTemplate):
    serializer_class = FollowSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "following__username", ]

    def get_queryset(self):
        queryset = Follow.objects.filter(following=self.request.user)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
