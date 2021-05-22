from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, permissions, viewsets

from .models import Follow, Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

User = get_user_model()


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

    def get_queryset(self):
        group_id = self.request.query_params.get("group", None)

        # if 'group' in URL parametes, return all posts for the group
        if self.request.method == "GET" and group_id:
            group = get_object_or_404(Group, pk=group_id)
            queryset = group.posts
        else:
            queryset = self.queryset

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username"]

    def get_queryset(self):
        queryset = Follow.objects.filter(following=self.request.user)

        following_user = self.request.data.get("following", None)
        search_user = self.request.query_params.get("search", None)

        if None not in [following_user, search_user]:
            raise exceptions.ValidationError(
                'can not use "following" and "search" at the same time'
            )

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
