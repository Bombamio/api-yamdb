from django.db.models import Avg
from django.contrib import admin
from .models import Category, Genre, Title, GenreTitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'titles_count')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def titles_count(self, obj):
        return obj.title_set.count()
    titles_count.short_description = 'Количество произведений'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'titles_count')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def titles_count(self, obj):
        return obj.titles.count()
    titles_count.short_description = 'Количество произведений'


class GenreTitleInline(admin.TabularInline):  # Tabular лучше чем Stacked
    model = Title.genre.through  # Используем through модель
    extra = 1
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'rating', 'genres_list')
    list_display_links = ('name',)
    list_editable = ('category', 'year')
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name', 'description', 'category__name')
    filter_horizontal = ('genre',)  # Удобный виджет для ManyToMany
    inlines = (GenreTitleInline,)  # Альтернатива filter_horizontal
    readonly_fields = ('rating',)

    fieldsets = (
        (None, {
            'fields': ('name', 'year', 'category', 'description')
        }),
        ('Жанры', {
            'fields': ('genre',)
        }),
        ('Дополнительно', {
            'fields': ('rating',),
            'classes': ('collapse',)
        }),
    )

    def genres_list(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    genres_list.short_description = 'Жанры'

    def rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(rating, 2) if rating else 'Нет отзывов'
    rating.short_description = 'Рейтинг'


# Если нужно отдельно управлять GenreTitle
@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_filter = ('genre',)
    search_fields = ('title__name', 'genre__name')
