from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from .models import Comment, Post, Group, Follow


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
        # queryset=User.objects.all()
    )

    following = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        # queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        #
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=['user', 'following'],
        #         message=''
        #     )
        # ]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("data can't be empty")
        return data
