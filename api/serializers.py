import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault()
    )

    following = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ['user', 'following']  # "__all__"
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message=''
            )
        ]

    def validate_following(self, following):
        if self.context.get('request').user == following:
            raise serializers.ValidationError(
                'You can not follow to yourself.'
            )
        return following


    # def validate(self, data):
    #     logging.warning(f'\t >> data: {data}')
    #     logging.warning(f'\t >> data keys: {[k for k in data.keys()]}')
    #     if not data:
    #         raise serializers.ValidationError("data can't be empty")
    #     if not data.get('following', None):
    #         raise serializers.ValidationError("following is required")
    #     return data