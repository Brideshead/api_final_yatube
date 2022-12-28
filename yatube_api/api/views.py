from typing import List

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from api.permissions import AuthorPermission
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для модели Group.

    Открытый доступ для всех только на
    чтение информации.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет для модели Follow.

    Авторизированные пользователи могут:

    1) get_queryset() - получать список подписчиков на автора.
    2) perform_create() - подписаться на автора.

    Удалять и обновлять комментарии могут только
    пользователи-авторы.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> None:
        """
        Запрашиваем список подписчиков на определенного автора.

        Returns:
            Если автор существует , возврашает список подписчиков.
        """
        return self.request.user.follower

    def perform_create(self, serializer: FollowSerializer) -> None:
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Post.

    Авторизированные пользователи могут:

    1) Читать посты;
    2) perform_create() - создавать новые посты.

    Удалять и обновлять посты могут только
    пользователи - авторы.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorPermission, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer) -> None:
        """
        Авт. пользователи могут создавать посты.

        Args:
            serializer: преобразование POST запроса
                в JSON объект со всей информацией о посте.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Comment.

    Авторизированные пользователи могут:

    1) get_post() - получать данные о посте.
    2) get_queryset() - получать список комментариев к посту.
    3) perform_create() - создавать комментарии.

    Удалять и обновлять комментарии могут только
    пользователи-авторы.
    """

    serializer_class = CommentSerializer
    permission_classes = [AuthorPermission, IsAuthenticatedOrReadOnly]

    def get_post(self) -> List[str]:
        """Полученние данных о посте."""
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id'),
        )

    def get_queryset(self) -> List[str]:
        """
        Запрашиваем список комментариев к посту.

        Returns:
            Если пост существует , возврашает список комментариев
            к определенному посту.
        """
        return self.get_post().comments

    def perform_create(self, serializer: CommentSerializer) -> None:
        """
        Авт. пользователи могут создавать комментарии.

        Args:
            serializer: преобразование POST запроса
                в JSON объект со всей информацией о комментарии.
        """
        serializer.save(author=self.request.user, post=self.get_post())
