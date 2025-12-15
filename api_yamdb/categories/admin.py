from django.contrib import admin
from django.db.models import Avg

from .models import Category, Genre, Title, GenreTitle


class BaseSlugAdmin(admin.ModelAdmin):
    '''Базовый класс для моделей со slug-полем.'''

    list_display = ('name', 'slug', 'titles_count')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def titles_count(self, obj):
        '''Возвращает количество произведений.'''
        # Универсальный подход через related_name
        return obj.titles.count()
    titles_count.short_description = 'Количество произведений'


@admin.register(Category)
class CategoryAdmin(BaseSlugAdmin):
    '''Админ-панель для категорий.'''
    pass


@admin.register(Genre)
class GenreAdmin(BaseSlugAdmin):
    '''Админ-панель для жанров.'''
    pass


class GenreTitleInline(admin.TabularInline):
    '''Inline для связи произведений с жанрами.'''

    model = Title.genre.through
    extra = 1
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    '''Админ-панель для произведений.'''

    list_display = ('name', 'year', 'category', 'rating', 'genres_list')
    list_display_links = ('name',)
    list_editable = ('category', 'year')
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name', 'description', 'category__name')
    inlines = (GenreTitleInline,)
    readonly_fields = ('rating',)

    fieldsets = (
        (None, {
            'fields': ('name', 'year', 'category', 'description')
        }),
        ('Дополнительно', {
            'fields': ('rating',),
            'classes': ('collapse',)
        }),
    )

    def genres_list(self, obj):
        '''Возвращает список жанров произведения в виде строки.'''
        return ", ".join([genre.name for genre in obj.genre.all()])
    genres_list.short_description = 'Жанры'

    def rating(self, obj):
        '''Рассчитывает средний рейтинг произведения.'''
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(rating, 2) if rating else 'Нет отзывов'
    rating.short_description = 'Рейтинг'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    '''Админ-панель для связи произведений и жанров (отдельная модель).'''

    list_display = ('title', 'genre')
    list_filter = ('genre',)
    search_fields = ('title__name', 'genre__name')
