from typing import Dict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализация модели Post."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация модели Group."""

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация модели Follow."""

    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Подписка на автора оформлена ранее!'),
            ),
        )

    def validate_following(self, data: Dict[str, str]) -> Dict[str, str]:
        """
        Проверка валидности данных.

        Пользователь не может подписаться на самого себя.

        Returns:
            Данные о пользователе и статусе.
        """
        if data == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!',
            )
        return data
