from django.contrib import admin
from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    '''Админ-панель для отзывов на произведения.'''
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    list_select_related = ('author', 'title')
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Админ-панель для комментариев к отзывам.'''
    list_display = ('review', 'author', 'pub_date')
    search_fields = ('text', 'author__username')
    list_select_related = ('author', 'review')
    ordering = ('-pub_date',)
