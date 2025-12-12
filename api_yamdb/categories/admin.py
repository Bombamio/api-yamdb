from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle


admin.site.empty_value_display = 'Не задано'


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name',
    )


class GenreTitleInline(admin.StackedInline):
    model = GenreTitle
    extra = 1


class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreTitleInline,)
    list_display = (
        'name',
        'year',
        'category',
        'genres_list',
    )
    list_editable = (
        'category',
    )
    search_fields = (
        'name',
        'category',
    )
    list_filter = ('year', 'category', 'genre',)
    list_display_links = ('name',)

    def genres_list(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)