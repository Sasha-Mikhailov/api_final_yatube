import logging

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import exceptions

from .models import Post, Group, Follow
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import \
    CommentSerializer, PostSerializer, GroupSerializer, FollowSerializer

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
        group_id = self.request.query_params.get('group', None)

        # if 'group' in URL parametes, return all posts for the group
        if self.request.method == 'GET' and group_id:
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
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        following_user = self.request.data.get('following', None)
        search_user = self.request.query_params.get('search', None)
        user_from_request = following_user or search_user or None

        if not None in [following_user, search_user]:
            raise exceptions.ValidationError(
                'can not use "following" and "search" at the same time'
            )

        if self.request.method not in permissions.SAFE_METHODS and not self.request.data:
            logging.warning(f'\t >> request data: {self.request.data}')
            raise exceptions.ValidationError

        if self.request.method == 'GET' and user_from_request:
            user = get_object_or_404(User, username=user_from_request)
            queryset = Follow.objects.filter(following=user)

        else:
            queryset = Follow.objects.filter(user=self.request.user)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
