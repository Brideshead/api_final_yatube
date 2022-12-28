from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Модель для хранения данных сообществ.

    Attributes:
        title: Название группы.
        slug: Уникальный адрес группы, часть URL.
        description: Текст, описывающий сообщество.
    """

    title = models.CharField('название группы', max_length=200)
    slug = models.SlugField('уникальный адрес', unique=True)
    description = models.TextField('описание группы')

    def __str__(self) -> str:
        """
        Возвращаем в консоль название группы.

        Returns:
            Название запрашиваемой группы в формате строки.
        """
        return self.title


class Post(models.Model):
    """
    Модель для хранения статей.

    Attributes:
        text: Текст.
        pud_date: Дата публикации статьи.
        author: Автор статьи, установлена связь с таблицей User,
            при удалении из таблицы User автора,
            также будут удалены все связанные статьи.
        group: Название сообщества, к которому относится статья,
            установлена связь с моделью Group, чтобы при добавлении
            новой записи можно было сослаться на данную модель.
        image: Возможность прикрепления изображения к посту.
    """
    text = models.TextField(
        'текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self) -> str:
        """
        Возвращаем в консоль название текст поста.

        Returns:
            Текст поста в формате строки.
        """
        return self.text


class Comment(models.Model):
    """
    Модель для хранения комментариев.

    Attributes:
        text: Текст.
        author: Автор статьи, установлена связь с таблицей User,
            при удалении из таблицы User автора,
            также будут удалены все связанные комментарии.
        post: Данные о посте, установлена связь с таблицей Post,
            при удалении из таблицы Post поста,
            также будут удалены все связанные комментарии.
        created: Дата добавления комментария.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        'текст комментария',
        help_text='Введите текст комментария',
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'


class Follow(models.Model):
    """
    Модель для хранения данных о подписке.

    Attributes:
        user: Пользователь, установлена связь с таблицей User,
            при удалении из таблицы User автора,
            также будут удалены данные о подписке.
        following: Статус подписки, установлена связь с таблицей User,
            при удалении из таблицы User автора,
            также будут удалены данные о статусе подписки.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow',
            ),
        )
