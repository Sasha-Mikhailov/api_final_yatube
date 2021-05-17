import logging

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import Post, Group, Follow
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import \
    CommentSerializer, PostSerializer, GroupSerializer

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
        # IsAdminOrReadOnly,
    ]



# class GroupPostsViewSet(viewsets.ModelViewSet):
#
#     serializer_class = GroupSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly,
#         # IsOwnerOrReadOnly,
#     ]
#
#     def get_post(self):
#         return get_object_or_404(Post, pk=self.kwargs["post_id"])
#
#     def get_queryset(self):
#         post = self.get_post()
#         group = get_object_or_404(Group, pk=post.group.id)
#         queryset = group.posts
#
#         if isinstance(queryset, QuerySet):
#             # Ensure queryset is re-evaluated on each request.
#             queryset = queryset.all()
#
#         return queryset
