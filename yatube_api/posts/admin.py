from django.contrib import admin

from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели 'Статьи' в интерфейсе админки.

    list_display: перечисляем поля, которые должны отображаться.
    search_fields: интерфейс для поиска по тексту постов.
    list_filter: фильтрация по дате.
    empty_value_display: вывод в поле текста '-пусто',
    если информация отсутствует.
    """

    list_display = (
        'pk',
        'pub_date',
        'author',
        'group',
        'image',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели 'Группы' в интерфейсе админки.

    list_display: перечисляем поля, которые должны отображаться.
    search_fields: интерфейс для поиска по тексту постов.
    prepopulated_fields: автоматическое создание SlugField
                    на базе заголовка.
    list_filter: фильтрация по дате.
    empty_value_display: вывод в поле текста '-пусто',
    если информация отсутствует.
    """

    list_display = (
        'title',
        'slug',
        'description',
    )
    prepopulated_fields = {
        'slug': ('title',),
    }
    search_fields = ('slug',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'
